#01/07/18

#ESTAS PRUEBAS ME AYUDAN A ENTENDER COMO FUNCIONA LA BIBLIOTECA
#PYAAF. LAMENTABLEMENTE, NO HAY TUTORIAL SOBRE SU USO ASÍ QUE
#ESTOY HACIENDO INGENIERIA REVERSA


#ESTA PRIMERA PARTE VIENE DE LA DOCUMENTACIÓN
import aaf

f = aaf.open("/home/nofi/DESARROLLO/PROYECTOS/ASISTENTE DE SONIDO/POSTPRODUCCIÓN/ESA/SAMPLES/NAVEGANTE/40 BRAMADORES INTRO.aaf", "r")

# get the main composition
main_compostion = f.storage.toplevel_mobs()[0]

# print the name of the composition
print ('NOMBRE: ' + main_compostion.name)

# AAFObjects have properties that can be accessed like a dictionary
# print out the creation time
print (main_compostion.comment_dict())

#print 'COMP MOB INFO'
print (main_compostion.properties())
print (main_compostion.all_keys())
for thing in main_compostion.all_keys():
    print (str(thing)+" "+str(main_compostion[thing].value))

# video, audio and other track types are stored in slots
# on a mob object.
n = 0

for slot in main_compostion.slots():
    segment = slot.segment
    print('CLASE DE SEGMENTO: ', segment.class_name)

    #LA MOVIE, AL PARECER, SE GUARDA COMO NESTEDSCOPE,
    #COMPACTAN TODOS LOS FRAGMENTOS EN UN SOLO ARCHIVO
    #PERO GUARDAN METADATA DE REFERENCIA A LOS ARCHIVOS
    #ORIGINALES. ESTO PUEDE SER DE MUCHA AYUDA PARA
    #APROVECHAR DATA DE LA EDICION (EJ, PARA DIVIDIR EN PLANOS
    #O BUSCAR EL NOMBRE DE PLANO Y ESC ORIGINAL Y/O LINKEAR
    #CON TOMA DE SONIDO DIRECTO

    if segment.class_name == 'NestedScope':

        for s in segment.segments():

            for c in s.components():
                #ME INTERESA SABER COMO ACCEDO AL NOMBRE DEL
                #ARCHIVO FUENTE
                if c.class_name == 'SourceClip':
                    print("SourceClip", c.source_ref.start_time)
                    #DESPUES DE MUCHAS PRUEBAS, ENCUENTRO LO QUE BUSCO:
                    #ASÍ SE ACCEDE AL NOMBRE DE ARCHIVO DE CADA
                    #FRAGMENTO QUE COMPONE LA MOVIE
                    print("SourceClip", c.resolve_ref().name)


                    print("SourceClip", c.mob_id)
                    print("SourceClip", c['MonoSourceSlotIDs'].value)

                    print("kEYS", c.all_keys())

                    for w in c.walk():
                        print ('w', w.source_ref)
                #print()
  #  print('KEYS ',segment.all_keys())

    elif segment.class_name == 'OperationGroup':

        if segment.media_kind == 'DataDef_Sound':
            for audio in segment.input_segments():
                print ("COMPONENTES: ", audio.components)
                for c in audio.components():
                    print('Componente audio ', c)
                    if c.class_name == 'OperationGroup':
                        for audio in c.input_segments():
                            print("AUDIO: ", audio.resolve_ref().name)

                    # ME INTERESA SABER COMO ACCEDO AL NOMBRE DEL
                    # ARCHIVO FUENTE
                   # if c.class_name == 'SourceClip':
                        #print("SourceClip", c.source_ref.start_time)
                        # DESPUES DE MUCHAS PRUEBAS, ENCUENTRO LO QUE BUSCO:
                        # ASÍ SE ACCEDE AL NOMBRE DE ARCHIVO DE CADA
                        # FRAGMENTO QUE COMPONE LA MOVIE
                    #    print("SourceClip Name", c.resolve_ref().name)

            print(segment.keys())
            print(segment['Parameters'])
            print(segment['DataDefinition'].value)
            #print("DATA: ", segment.slot_id)







    print (segment.media_kind)
#    print (segment.length)
#    print (segment.all_keys())
#    print ('Start: ' , segment.get_value('Length'))
