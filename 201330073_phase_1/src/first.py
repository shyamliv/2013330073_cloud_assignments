from flask import Flask, jsonify
from flask import request
import json
import settings
import sys
import create_vm
import destroy_vm
import uuid
import subprocess
app = Flask(__name__)

@app.route('/server/vm/create', methods=['GET'])
def create():
	name = request.args.get('name')
	inst = request.args.get('instance_type')
	img = request.args.get('image_id')
	vm = {}
	vm['name'] = name
	vm['instance_type'] = inst
	vm['image_id'] = img
	return jsonify(create_vm.create(vm))

@app.route('/server/vm/query', methods=['GET'])
def query():
	vmid = request.args.get('vmid')
	vm_found={}
	for vm in settings.vm_list:
		if vm[0]==int(vmid):
			vm_found['vmid']=vm[0]
			vm_found['name']=vm[1]
			vm_found['instance_type']=vm[2]
			vm_found['pmid']=vm[3]
			break
	return jsonify(vm_found)

@app.route('/server/vm/destroy', methods=['GET'])
def destroy():
	vmid = request.args.get('vmid')
	return jsonify(destroy_vm.destroy(vmid))

@app.route('/server/vm/types', methods=['GET'])
def types():
	return jsonify(settings.Type)

@app.route('/server/pm/list', methods=['GET'])
def list_pm():
	pm = []
	for pms in settings.machine_list:
		pm.append(pms[3])
	return jsonify({'pm' : pm})

@app.route('/server/pm/listvms', methods = ['GET'])
def list_vm():
	pm_id=int(request.args.get('pmid'))
	vm=[]
	print settings.vm_list
	for vms in settings.vm_list:
		if vms[3]==pm_id:
			vm.append(vms[0])
	return jsonify({"vmids":vm})	

@app.route('/server/pm/query', methods=['GET'])
def pm_query():
	pmid=int(request.args.get('pmid'))
	pm={}
	capacity={}
	free={}
	pm['pmid']=pmid
	count=0
	for vms in settings.vm_list:
		if vms[3]==pmid:
			count=count+1
	pm['vms']=count
	mach = settings.machine_list[pmid-1]
	user=mach[0]
	ip=mach[1]
	cpu = int(subprocess.check_output("ssh "+user+"@"+ip+" nproc",shell=True))
	ram = subprocess.check_output("ssh "+user+"@"+ip+" free -m | grep 'Mem'", shell=True)
	ram=ram.split()
	capacity['cpu']=cpu
	tot_ram =int(ram[1])
	capacity['ram']=tot_ram
	free_ram = int(ram[3])
	free['ram']=free_ram
	disk=subprocess.check_output("ssh "+user+"@"+ip+" df -h --total | grep 'total'",shell =True)
	disk =disk.split()
	tot_disk = int(disk[1].split('G')[0])
	free_disk = int(disk[3].split('G')[0])
	capacity['disk']=tot_disk
	free['disk']=free_disk
	socket = subprocess.check_output("ssh "+user+"@"+ip+" lscpu | grep 'Socket'",shell=True)
	socket = int(socket.split()[1])
	core = subprocess.check_output("ssh "+user+"@"+ip+" lscpu | grep 'Core'",shell=True)
	core= int(core.split()[3])
	free_cpu = socket*core
	free['cpu']= cpu-free_cpu
	pm['capacity']=capacity
	pm['free']=free
	print capacity
	print free
	return jsonify(pm)

def get_machines(filename):
	fp=open(filename)
	lines=fp.readlines()
	i=1
	for line in lines:
		line=line[:-1]
	    	dummy=line.split("@")
	    	dummy[1].strip()
	    	dummy.append(uuid.uuid4())
	    	dummy.append(i)
	    	i=i+1
	    	settings.machine_list.append(dummy)
#	print machine_list
@app.route('/server/image/list',methods=['GET'])
def img_query():
	imag=[]
	img={}
	for im in settings.imageid_list:
		img['id']=im[0]
		img['name']=im[1]
		imag.append(img)
	return jsonify({"images":imag})
def get_images(filename):
	fp=open(filename)
	lines=fp.readlines()
	trial=[]
	settings.count=1
	for line in lines:
		line=line[:-1]
		dummy=line.split("@")
		trial.append(dummy[0])
		t=dummy[1].split(":")
		trial.append(t[0])
		trial.append(t[1])
		prac=[]
		prac.append(settings.count)
		prac.append(t[1].split("/")[-1])
		settings.imageid_list.append(prac)
		settings.count=settings.count+1
		settings.image_list.append(trial)
#	print settings.image_list
#	print settings.imageid_list

def get_types(filename):
	vMTypeFile = open(filename)
	vMLines=vMTypeFile.readlines()
	vMType=unicode(''.join( map(lambda lin: lin.strip(),vMLines) )  )
	settings.Type=json.loads(vMType)
if __name__ == "__main__":
	if len(sys.argv)<4:
		print "Format is ./script pm_file image_file type_file"
		exit(1)
	var1=sys.argv[1]
	var2=sys.argv[2]
	var3=sys.argv[3]
	machine_list=[]
	get_machines(var1)
	get_images(var2)
	get_types(var3)
	app.run(debug=True)
