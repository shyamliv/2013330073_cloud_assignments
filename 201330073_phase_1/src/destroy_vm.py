import libvirt
import first
import settings
settings.init()
def destroy(vm_id):
	count=0
	for vm in settings.vm_list:
		if vm[0]==int(vm_id):
			break
		count=count+1
	print vm[3]
	pm = settings.machine_list[vm[3]-1]
	user = pm[0]
   	ip = pm[1]
	print settings.vm_list
	connect=libvirt.open('remote+ssh://'+user+'@'+ip+'/')
	vm_found = connect.lookupByName(vm[1])
	try:
		if vm_found.isActive():
			vm_found.destroy()
		vm_found.undefine()
		del settings.vm_list[count]
		return {"status":"1"}
	except:
		return {"status":"0"}				
