def analyze_line(line):
	

def image_splitting():
	strace_output = ""
	with open(strace_output,'r',encoding = 'utf-8') as f:
		line = f.readline()
		while(line):
			analyze_line(line)
			line = f.readline()
		

if __name__ == '__main__':
	image_splitting()
