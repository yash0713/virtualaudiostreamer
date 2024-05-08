import subprocess
import audioop

try:
    print('-' * 40)
    print('Initiating virtual audio cable ...')
    cmd1 = ['pacmd', 'load-module', 'module-null-sink', 'sink_name=virtual_stream_sink', 'sink_properties=device.description=virtual_stream']
    subprocess.Popen(cmd1)
    subprocess.Popen('pavucontrol')

    '''
    Create a virtual input stream which can take audio input from system.
    '''
    cmd2 = ['arecord', '-f', 'cd', '-']
    process1 = subprocess.Popen(cmd2, stdout=subprocess.PIPE)

    '''
    Create a virtual output stream which can direct the output to device.
    '''

    cmd3 = ['aplay', '-f', 'cd', '-']
    process2 = subprocess.Popen(cmd3,stdin=process1.stdout)

    print('-' * 40)
    print('Use CTRL+C to terminate the program and terminate the virtual stream')
    print('')
    print('-' * 40)
    input()

except EOFError:
    print('EOF Error')

except KeyboardInterrupt:
    print()
    print('Exiting the program')
    
    uncmd1 = ['pactl', 'list', 'short', 'modules']
    uncmd2 = ['grep', 'sink_name=virtual_stream_sink']
    uncmd3 = ['cut', '-f1']
    uncmd4 = ['xargs', '-L1', 'pactl', 'unload-module']

    endprocess1 = subprocess.Popen(uncmd1, stdout=subprocess.PIPE)
    endprocess2 = subprocess.Popen(uncmd2, stdin=endprocess1.stdout, stdout=subprocess.PIPE)
    endprocess3 = subprocess.Popen(uncmd3, stdin=endprocess2.stdout, stdout=subprocess.PIPE)
    endprocess4 = subprocess.Popen(uncmd4, stdin=endprocess3.stdout)

    killcmd = ['pkill', 'arecord'] # to kill the stream
    closefin = subprocess.Popen(killcmd)
