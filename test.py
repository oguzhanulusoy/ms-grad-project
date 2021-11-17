import os
install = "pip install diagrammer/yuml.me/yuml"
returned_value = os.system(install)
cmd = "echo \"[You]-(Draw Diagrams)\" | ./yuml -t usecase -s scruffy -o diagram654.png"
returned_value = os.system(cmd)