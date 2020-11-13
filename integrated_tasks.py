import os,webbrowser
print("\n\t\t*********** Assist U ***********\n")

#--------------------------------------------------------------
#*********************HADOOP SETUP*********************
def hadoop_setup():

#****************************************
#Creating template for configuration files
	file_1 = open("hdfs-site.xml","w")

	file_1.write('<?xml version="1.0"?>\n<?xml-stylesheet type="text/xs1”href="configuration.xsl"?>\n\n<!-- Put site-specific property overrides in this file. -->')

	file_1.close()
#****************************************

	print("****************** Welcome to Hadoop Setup*******************\nMenu : \n")
	print("\t1)Configuring master node\n\t2)Configuring slavenode\n\t3)Configuring as client\n\t4.EXIT")

#****************************************
#Configuring name node
	def creating_master():

		ip_master = input("enter the ip of master: ")
		port = input("enter the port number of master: ")
		dir = input("enter the name of directory: ")
		os.system("sudo mkdir /{}".format(dir))

		file_1 = open("hdfs-site.xml", "r" )

		lines = file_1.readlines()

		file_1.close()

		new = "".join(lines)

#hdfs-site.xml configuration
		hdfs = open("hdfs-site.xml","w")
		hdfs.write(new + "\n<configuration>\n" + "<property>\n" +
		"<name>dfs.name.dir</name>\n" + "<value>/{}</value>\n".format(dir) +
		"</property>\n" + "</configuration>\n")
		hdfs.close()

#core-site.xml configuration
		core = open("core-site.xml", "w")
		core.write(new+"\n<configuration>\n"+"<property>\n"
	+"<name>fs.default.name</name>\n"+"<value>hdfs://{}:{}</value>\n".format(ip_master,port)+"</property>\n"+"</configuration>\n")

		core.close()

#Setting up namenode
		os.system("sudo cp hdfs-site.xml /etc/hadoop/hdfs-site.xml")
		os.system("sudo cp core-site.xml /etc/hadoop/core-site.xml")
		os.system("sudo hadoop namenode -format")
		os.system("sudo hadoop-daemon.sh start namenode")
		os.system("sudo jps")

#****************************************

#Configuring slave

	def creating_slave():

		no_slaves=input("How many slaves you wanted to be created")
		
		for i in range(0,no_slaves):
			ip_master = input("enter the ip of master: ")
			
			port = input("enter the port number of master")
			ip_slave = input("enter the ip of slave: ")

			dir = input("enter the directory for slavenode: ")
			os.system("sudo ssh {} mkdir /{}".format(ip_slave,dir))
			file = open("hdfs-site.xml", "r")

			lines = file.readlines()

			file.close()

			new = "".join(lines)

#Configuring hdfs-site for slave
			hdfs = open("hdfs-site.xml", "w")
			hdfs.write(new +"\n<configuration>\n" + "<property>\n" +
			"<name>dfs.data.dir</name>\n" + "<value>/{}</value>\n".format(dir) +
			"</property>\n" +"</configuration>\n")

			hdfs.close()

#configuring core-site.xml for slave
			core = open("core-site.xml", "w")

			core.write(new+"\n<configuration>\n"+"<property>\n"
		+"<name>fs.default.name</name>\n"+"<value>hdfs://{}:{}</value>\n".format(ip_master,port) + "</property>\n"+"</configuration>\n")

			core.close()

#setting up datanode
			os.system("sudo scp hdfs-site.xml core-site.xml {}:/root".format(ip_slave))

			os.system("sudo ssh {} cp hdfs-site.xml /etc/hadoop/hdfs-site.xml".format(ip_slave))

			os.system("sudo ssh {} cp core-site.xml /etc/hadoop/core-site.xml".format(ip_slave))
			
			os.system("sudo hadoop-daemon.sh start datanode")
		
			os.system("hadoop dfsadmin -report")


#****************************************
#Configuring client

	def creating_client():
			ip_master = input("enter the ip of master: ")
			
			port = input("enter the port number of master: ")
			ip_client = input("enter the ip of Client: ")

			file = open("hdfs-site.xml", "r")

			lines = file.readlines()

			file.close()

			new = "".join(lines)

#configuring core-site.xml for client
			core = open("core-site.xml", "w")

			core.write(new+"\n<configuration>\n"+"<property>\n"
		+"<name>fs.default.name</name>\n"+"<value>hdfs://{}:{}</value>\n".format(ip_master,port) + "</property>\n"+"</configuration>\n")

			core.close()

#setting up client
			os.system("sudo scp core-site.xml {}:/root".format(ip_client))

			os.system("sudo ssh {} cp core-site.xml /etc/hadoop/core-site.xml".format(ip_client))

#Client operations
			os.system("hadoop fs -ls")

				
			print("\t\t\tTasks\n\t1.Upload file\n\t2.Removing file\n\t3.Exit\n")
		
			while(1):
				choice_1=input("Enter choice:")
#file upload operation
				if choice_1 == '1':
					filename=input("file to be uploaded.{extension} : ")
					print("Do you want to change block size : {Y|N}")
					yes_no = input("#").capitalize()

					bytes = input("Input block size in Bytes")
#changing block size
					if(yes_no == "Y"):
						os.system(f"sudo hadoop fs -D dfs.block.size={bytes} -put {filename}")
					else:
						os.system(f"sudo hadoop fs -put {filename} /")
#removing file					
				elif choice_1 == '2':
					filename=input("file to be deleted.{extension} :")
					os.system(f"sudo hadoop fs -rm /{filename}")
				
				elif choice_1 == '3':
					exit()

#****************************************
					
	while(1):
		choice = input("enter your choice: ")

		if choice == '1':
			creating_master()
		elif choice == '2':
			creating_slave()
		elif choice == '3':
			creating_client()
		else:
			exit()

#--------------------------------------------------------------
#*******************LVM*******************
def lvm():
	
	print("Welcome to my LVM ")
	print("\n1.create LVM\n2.extend partition\n3.Add more device to Volume group\n4.EXIT")

#*********************************
#Volume group creation
	def create_volume_group():

		print("Listing the devices mounted on this host")
		os.system("sudo fdisk -l")

		storages=input("enter path of storage devices /dev/sda : ").split()
		print("\n")

		for i in storages:
			os.system("sudo pvcreate {}".format(i))
		print("\n")

		vg_name=input("enter name of virtual group : ")
		
		cmd = ''
		for i in storages:
			cmd = cmd + ' ' + i 

#volume group created			
		os.system("sudo vgcreate {} {}".format(vg_name,cmd))
		print("\n")

		size=input("enter size of partition :")
		name_lvm=input("Enter the name of partition :")
		print("\n")

#logical volume created
		os.system("sudo lvcreate --size {}G --name {} {}".format(size,name_lvm,vg_name))

#formated created volume
		os.system("sudo mkfs.ext4 /dev/{}/{}".format(vg_name,name_lvm))
		print("\n")

#Mounting
		mount_point=input("Enter the mount point name : ")
		print("\n")
		os.system("sudo mkdir /{}".format(mount_point))
		os.system("sudo mount /dev/{}/{}/{}".format(vg_name,name_lvm,mount_point))
	
#*****************************************
#Partition extension
	def extend_partition_size():

		size=input("Enter the size ")
		vgname=input("Enter the name of vg group")
		name=input("Name of partition")

#logical volume extended
		os.system("sudo lvextend --size +{}G /dev/{}/{}".format(size,vgname,name))

#updating partition table
		os.system("sudo resize2fs /dev/{}/{}".format(vgname,name))

#******************************************

#Volume group extension
	def extend_volume_group():

		print("List of devices you have :\n")
		os.system("sudo fdisk -l")
		print("\n\n")

		vg_name=input("Enter the name of vg group :# ")
		new_hd=input("Enter new HD device (/dev/sdd.../dev/sdc) :# ")

#physical volume creation
		os.system("sudo pvcreate {}".format(new_hd))
#volume group extension
		os.system("sudo vgextend {} {}".format(vg_name,new_hd))
		print("\nDo you want to extend space of LV(Y/N) : ")
		choice=input("##").capitalize()	
		if(choice=="Y"):
			size=int(input("Enter size to be extended for partition :"))
			name=input("Name of partition :")
#logical volume size provision
			os.system("sudo lvextend --size +{} /dev/{}/{}".format(size,vgname,name))

#updating partition table
			os.system("sudo resize2fs /dev/{}/{}".format(vgname,name))
			print("\n")
			print("Size of LV increased! by {}".format(size))
		else:
			print("Volume group extended successfully")
			exit()	
#**********************************************

	while 1:		
		choice = int(input ("enter ur choice : "))

		if(choice==1):
			create_volume_group()
				
		elif(choice==2):
			extend_partition_size()
			
		elif(choice==3):
			extend_volume_group()
			
		else:
			exit()
		

#--------------------------------------------------------------

#************AWS************
def aws():
	print("Loading .....AWS CLI (Script in development mode)")
	print("------------------------------------------------\n")
	print("*****WELCOME TO AWS CLI*****")
	print("\n\nNOTE: Only AMI LINUX Available right now in ec2-free-tier\n")

#configuring AWS CLI
	os.system("aws configure")

	print("----Service List----\n")
	print("1.EC2\n2.CloudWatch\n...many more to come")
	choice = input("#")

#EC2 service
	def ec2_service():

		print("1.Launch instance \n2.create volume \n3.Attach volume \n4.EXIT\n")

		choice_1 = input("#")

		if choice_1 == '1':
			print("\n")
#Launching instance
			os.system("aws ec2 run-instances --image-id ami-0e306788ff2473ccb --count 1 --instance-type t2.micro --key-name Mykey --security-group-ids sg-01cae87e35ff1fddb --subnet-id subnet-21212849")
	
#Creating volume		
		elif choice_1 == '2':
			os.system("aws ec2 create-volume \--volume-type gp2 \--size 30 \--availability-zone ap-south-1a")

#Attach volume to existing instance
		elif choice_1 == '3':
			os.system("aws ec2 attach-volume --volume-id vol-0174c90d2a3035f5e --instance-id i-0104eecbd16db9620 --device /dev/sdf")

		else:
			exit()
#************************************************************
	while 1:
		if choice == '1': 
			ec2_service()
		elif choice == '2':
			print("unavailable right now")
		else:
			print("Not available ,visit after some time......")
			exit()

#--------------------------------------------------------------
#**********DOCKER***************
def docker():
		
	print("Welcome to Docker world")
	def docker_auto():
		#os.chdir("/etc/yum.repos.d")
		#os.system("touch docker-ce.repo")
		os.system("sudo dnf install docker-ce --nobest")
		os.system("sudo systemctl start docker")
		print("Docker Info :\n")
		os.system("sudo docker info")
		#print("Visiting website..........")
		#webbrowser.open("https://hub.docker.com/search?q=&type=image")

		iso_name=input("Enter iso file name")
		iso_version=input("Enter version")
		container=iso_name+':'+iso_version
		
		while(1):
			choice = int(input("\n1.Pull iso image.\n2.Install OS.\n3.Check running OS.\n4.Shutdown OS.\n5.Start OS.\n0.EXIT\n#"))
			#iso_image pull	
			if(choice==1):	
				os.system("sudo docker pull {}".format(container))

			#installing os
			elif(choice==2):
				print("Installing the {} OS".format(iso_name))
				os.system("sudo docker run -it {}".format(container))

			#Checking running os
			elif(choice==3):
				print("Checking OS running on docker")
				os.system("sudo docker ps")
			
			#Shutdown OS
			elif(choice==4):
				print("Shutdown OS")
				os.system("sudo docker ps -a -q")
				os_name=input("Enter OS name")
				os.system("sudo docker stop {}".format(os_name))

		#Starting os
			elif(choice==5):
				print("Starting OS")	
				os_name=input("Enter OS name")
				os.system("sudo docker start {}".format(os_name))
				os.system("sudo docker attach {}".format(os_name))
			else:
				exit()
	docker_auto()

#--------------------------------------------------------------

#*************Configure Web-Server****************

def web_server():	
	def web_server_config():

			#os.system("yum install httpd")
			#os.system("systemctl start httpd")
			#print("Server started")

			choice=input("Do you want to configure web server (Y|N) : ").capitalize()

			if(choice=="Y"):
				dir_name=input("Enter file name: ")
				path = "/var/www/html"
				os.chdir(path)
#configure file
				os.system("gedit {}".format(dir_name))
				print("Configured successfully")

				print("Do you want to access ur work on server(Y/N): ")
				choice_1=input("# ").capitalize()

				if(choice_1=="Y"):
					webbrowser.open("http://192.168.0.166/{}".format(dir_name))
				else:
					exit()

			else:
				exit()
	web_server_config()
#--------------------------------------------------------------
#--------------------------------------------------------------

#Main function
def main():
	print("\t1.Hadoop-Setup\n\t2.LVM\n\t3.AWS\n\t4.Docker\n\t5.Configure web server\n\t0.EXIT\n")
	get=int(input("# "))
	print("\n")

	if get == 1:
		hadoop_setup()
	elif get == 2:
		lvm()
	elif get == 3:
		aws()
	elif get == 4:
		docker()
	elif get == 5:
		web_server()
	else:
		exit()
main()
#--------------------------------------------------------------
