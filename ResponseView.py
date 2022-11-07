import sys
import SetCurrentDir  # Sí se usa! Hace inicializaciones de directorio.
import KhRequest

if len(sys.argv) == 1:
    print("""
    ResponsiveView
    --------------
    
    Programa para visualizar archivos del tipo .response
    
    Se visualiza el archivo pasado como parámetro. Lo que permite vincular la extensión
    .response con ResponsiveView
    
    c:> ResponsiveView c:\demo.response
    
    Los archivos .response son generados vaciando un objeto Python del tipo Response
    del módulo requests. Los objetos son guardados a disco usando pickle para su 
    posterior recuperación.
    """)
    sys.exit()

response = KhRequest.load_response(sys.argv[1])
print(KhRequest.format_pretty_response(response))
