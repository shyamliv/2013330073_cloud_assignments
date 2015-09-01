import libvirt
import first
import os
from uuid import uuid4
from random import random
import subprocess
import first
import settings
settings.init()
def create_xml(hypervisor,vm_name,ram,uuid,cpu,arch_type,driver,source_path):
    xml = "<domain type='" + hypervisor + 			\
	    "'><name>" + vm_name + "</name>				\
		<uuid>" + uuid + "</uuid> \
	      <memory>" + ram + "</memory>					\
	      <vcpu>" + cpu + "</vcpu>						\
	      <os>							\
	        <type arch='" + arch_type + "' machine='pc'>hvm</type>		\
		<boot dev='hd'/>					\
	      </os>							\
	      <features>						\
	        <acpi/>							\
          	<apic/>							\
	      	<pae/>							\
	      </features>						\
              <clock offset='utc'/>                                     \
	      <on_poweroff>destroy</on_poweroff>			\
  	      <on_reboot>restart</on_reboot>				\
	      <on_crash>restart</on_crash>				\
	      <devices>							\
	        <disk type='file' device='disk'>			\
		<driver name=" + driver + " type='raw'/>			\
		<source file='" + source_path + "'/>		\
		<target dev='hda' bus='ide'/>				\
		<address type='drive' controller='0' bus='0' unit='0'/>	\
		</disk>							\
	      </devices>						\
   	      </domain>"

    return xml

def create(attr):
	name = attr["name"]
	inst_type= int(attr["instance_type"])	
	img_id = int(attr["image_id"])
	vm_ram = settings.Type['types'][inst_type-1]['ram']
	vm_ram = vm_ram*1024
	vm_cpu = int(settings.Type['types'][inst_type-1]['cpu'])
	total_pm=1
	pm = settings.machine_list[settings.pm_id-1]
	user = pm[0]
	ip = pm[1]
	avail_cpu=int(subprocess.check_output("ssh " + user+"@"+ip+" nproc", shell=True))
	free_space=(subprocess.check_output("ssh "+user+"@"+ip+" free -m", shell=True))
	free_space=free_space.split("\n")
	free_space=free_space[1].split()
	avail_ram=int(free_space[3])
	avail_ram = avail_ram*1024
	new_pmid=settings.pm_id - 1
	while(avail_cpu < vm_cpu or avail_ram < vm_ram):
		new_pmid= (new_pmid + 1)%(len(settings.machine_list))
		total_pm = total_pm + 1
		if(total_pm > len(settings.machine_list)):
			return {"Error" :" Specs could not be satisfied; Virtual Machine cannot be created" }
		pm = settings.machine_list[new_pmid]
		user = pm[0]
		ip = pm[1]
		avail_cpu=int(subprocesses.check_output("ssh "+user+"@"+ip+" nproc", shell=True))
		free_space=(subprocess.check_output("ssh "+user+"@"+ip+" free -m", shell=True))
		free_space=free_space.split("\n")
		free_space=free_space[1].split()
		avail_ram=int(free_space[3])
		avail_ram=avail_ram*1024
	
	settings.vm_id=settings.vm_id+1
	settings.vm_list.append([settings.vm_id,name,inst_type,settings.pm_id])
	new_pmid = (new_pmid + 1 )%(len(settings.machine_list))
	settings.pm_id = new_pmid + 1
	uid = str(uuid4())
	var = "remote+ssh://"+user+"@"+ip+"/"
	connect = libvirt.open("remote+ssh://" + user + "@" + ip + "/")
	sys_info = connect.getCapabilities()
	emulator_path= sys_info.split("emulator>")
	emulator_path = emulator_path[1].split("<")[0]
	emulator=sys_info.split("<domain type=")
	emulator=emulator[1].split(">")[0]
	arch_type= sys_info.split("<arch>")
	arch_type = arch_type[1].split("<")[0]
	
	im = settings.image_list[img_id-1]
	im_user = im[0]
	im_ip = im[1]
	im_path = im[2]
	print im_path
	im_name=settings.imageid_list[img_id-1][1]
	os.system("scp "+im_user+"@"+im_ip+":"+im_path+" ~/"+im_name)
	os.system("scp ~/"+im_name+"/ "+user+"@"+ip+":/home/"+user+"/"+im_name)
	source = "/home/"+user+"/"+im_name
	call = connect.defineXML(create_xml(connect.getType().lower(),str(name),str(vm_ram),uid,str(vm_cpu),arch_type,emulator,str(source)))
	try:
		call.create()
		return {"vmid":settings.vm_id}
	except:
		return {"vmid": 0}
