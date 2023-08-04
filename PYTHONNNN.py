import arcpy
def ScriptTool(param0, param1, param2, param3, param4, param5, param6, param7, param8, param9, param10, param11):
    return
if __name__ == '__main__':
    param0 = arcpy.GetParameterAsText(0)
    param1 = arcpy.GetParameterAsText(1)
    param2 = arcpy.GetParameterAsText(2)
    param3 = arcpy.GetParameterAsText(3)
    param4 = arcpy.GetParameterAsText(4)
    param5 = arcpy.GetParameterAsText(5)
    param6 = arcpy.GetParameterAsText(6)
    param7 = arcpy.GetParameterAsText(7)
    param8 = arcpy.GetParameterAsText(8)
    param9 = arcpy.GetParameterAsText(9)
    param10 = arcpy.GetParameterAsText(10)
    param11 = arcpy.GetParameterAsText(11)
    
    ScriptTool(param0, param1, param2, param3, param4, param5, param6, param7, param8, param9, param10, param11)
# Parámetro 0 = capa de entrada red hidrográfica
# Parámetro 1 = campo para consulta sql de selección (cod_dren_tip)
# Parámetro 2 = nombre de salida de la capa 1 (quebradas de la comuna)
# Parámetro 3 = Nombre de salida de capa 2 (puntos a lo largo de las quebradas)
# Parámetro 4 = Capa de manzanas de la florida
# Parámetro 5 = Directorio de salida buf 25
# Parámetro 6 = Directorio de salida buf 50
# Parámetro 7 = Directorio de salida buf 75
# Parámetro 8 = Directorio de salida buf final
# Parámetro 9 = Directorio de salida union manzanas y buf final
# Parámetro 10 = Tabla de población
################################################################################################################
# DEFINICION DE GEOPROCESOS A UTILIZAR
# Definición de geoproceso de selección
#SELECT(CAPA_ENTRADA,PARAMETRO_DE_SELECCION,CAMPO_DEL_PARAMETRO_SELECCION,DIRECCION_DE_SALIDA)
def select(layer,parametro,campo_parametro,output_dir):
    whClause =''+campo_parametro+'={}'.format(str(parametro))
    arcpy.analysis.Select(layer,
                          output_dir,
                          whClause)
    return
# Definición de generación de puntos a lo largo de una línea
# PUNTOS(LINEAS_DE_ENTRADA, DIRECCIÓN_SALIDA)
def puntos(layer,output):
    arcpy.management.GeneratePointsAlongLines(layer,
                                              output,
                                              "DISTANCE",
                                              "800 Unknown",
                                              None,
                                              "END_POINTS")    
    return
# Definición de lineas agua abajo a partir de puntos
# PUNTOS(PUNTOS DE ENTRADA)
def traz_abajo(layer):
    arcpy.sa.TraceDownstream_agolservices(layer,
                                   '',
                                   "FINEST",
                                   False)
    
##    layer = arcpy.agolservices.TraceDownstream(name,
##                                       '',
##                                       "FINEST",
##                                       False)
    return layer
# Definición de capa a capa
# FCF(CAPA_ENTRADA, DIRECCION_DE_SALIDA, NOMBRE_CAPA_NUEVA)
def fcf(layer,output,name):
    arcpy.conversion.FeatureClassToFeatureClass(layer,
                                                output,
                                                name)
    return
# Definición de buffer
# BUF(CAPA_PARA_BUFF, DIRECTORIO_DE_SALIDA, DISTANCIA)
def buf(layer, output_layer, distance):
    arcpy.analysis.Buffer(layer,
                          output_layer, 
                          distance, 
                          "FULL", 
                          "ROUND", 
                          "ALL", 
                          None, 
                          "PLANAR")
    return
# Creación de definición para generar un geoprocesamiento de fusión
# FUSION(CAPA_ENTRADA_1, CAPA_ENTRADA_2, CAPASA_ENTRADA_3, DIRECTORIO_SALIDA)
def fusion(layer_1,layer_2,layer_3,param):
    layers = "" + layer_1 + ";" + layer_2 + ";" + layer_3 + ""
    arcpy.management.Merge(layers,
                           param,
                           "",
                           "NO_SOURCE_INFO")
    return
# Creación de definición para unión de capas
# JOIN(CAPA_DE_UNIÓN_1, CAPA_DE_UNIÓN_2, DIRECTORIO_DE_SALIDA)
def join(layer_1,layer_2,directorio):
    arcpy.analysis.SpatialJoin(layer_1,
                           layer_2,
                           directorio,
                           "JOIN_ONE_TO_MANY",
                           "KEEP_ALL",
                           'FID_1 "FID_1" true true false 4 Long 0 0,First,#,man_lf,FID_1,-1,-1;REGION "REGION" true true false 2 Text 0 0,First,#,man_lf,REGION,0,2;NOM_REGION "NOM_REGION" true true false 55 Text 0 0,First,#,man_lf,NOM_REGION,0,55;PROVINCIA "PROVINCIA" true true false 3 Text 0 0,First,#,man_lf,PROVINCIA,0,3;NOM_PROVIN "NOM_PROVIN" true true false 23 Text 0 0,First,#,man_lf,NOM_PROVIN,0,23;COMUNA "COMUNA" true true false 5 Text 0 0,First,#,man_lf,COMUNA,0,5;NOM_COMUNA "NOM_COMUNA" true true false 20 Text 0 0,First,#,man_lf,NOM_COMUNA,0,20;DISTRITO "DISTRITO" true true false 2 Short 0 0,First,#,man_lf,DISTRITO,-1,-1;LOCALIDAD "LOCALIDAD" true true false 2 Short 0 0,First,#,man_lf,LOCALIDAD,-1,-1;ENTIDAD_MA "ENTIDAD_MA" true true false 2 Short 0 0,First,#,man_lf,ENTIDAD_MA,-1,-1;CATEGORIA "CATEGORIA" true true false 2 Short 0 0,First,#,man_lf,CATEGORIA,-1,-1;NOM_CATEGO "NOM_CATEGO" true true false 2 Text 0 0,First,#,man_lf,NOM_CATEGO,0,2;MANZENT_I "MANZENT_I" true true false 14 Text 0 0,First,#,man_lf,MANZENT_I,0,14;Shape__Are "Shape__Are" true true false 8 Double 0 0,First,#,man_lf,Shape__Are,-1,-1;Shape__Len "Shape__Len" true true false 8 Double 0 0,First,#,man_lf,Shape__Len,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,man_lf,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,man_lf,Shape_Area,-1,-1;COD_MANZ "COD_MANZ" true true false 8 Double 0 0,First,#,man_lf,COD_MANZ,-1,-1;Shape_Length_1 "Shape_Length" false true true 8 Double 0 0,First,#,buf_final,Shape_Length,-1,-1;Shape_Area_1 "Shape_Area" false true true 8 Double 0 0,First,#,buf_final,Shape_Area,-1,-1',
                           "INTERSECT",
                           None,
                           '')
    return
# Creación de definición para unión de campos
# UNION_CAMP(CAPA_DE_ENTRADA, TABLA, CAMPO_DE_UNION)
def union_camp(layer, tabla, campo):
    arcpy.management.JoinField(layer,
                           campo,
                           tabla,
                           campo,
                           None,
                           "USE_FM",
                           'FID "FID" true true false 255 Text 0 0,First,#,poblacion_la_florida,FID,0,255;the_geom "the_geom" true true false 32777 Text 0 0,First,#,poblacion_la_florida,the_geom,0,32777;FID_1 "FID" true true false 4 Long 0 0,First,#,poblacion_la_florida,FID_1,-1,-1;REGION "REGION" true true false 255 Text 0 0,First,#,poblacion_la_florida,REGION,0,255;NOM_REGION "NOM_REGION" true true false 255 Text 0 0,First,#,poblacion_la_florida,NOM_REGION,0,255;PROVINCIA "PROVINCIA" true true false 255 Text 0 0,First,#,poblacion_la_florida,PROVINCIA,0,255;NOM_PROVIN "NOM_PROVIN" true true false 255 Text 0 0,First,#,poblacion_la_florida,NOM_PROVIN,0,255;COMUNA "COMUNA" true true false 255 Text 0 0,First,#,poblacion_la_florida,COMUNA,0,255;NOM_COMUNA "NOM_COMUNA" true true false 255 Text 0 0,First,#,poblacion_la_florida,NOM_COMUNA,0,255;DISTRITO "DISTRITO" true true false 4 Long 0 0,First,#,poblacion_la_florida,DISTRITO,-1,-1;LOCALIDAD "LOCALIDAD" true true false 4 Long 0 0,First,#,poblacion_la_florida,LOCALIDAD,-1,-1;ENTIDAD_MA "ENTIDAD_MA" true true false 4 Long 0 0,First,#,poblacion_la_florida,ENTIDAD_MA,-1,-1;CATEGORIA "CATEGORIA" true true false 4 Long 0 0,First,#,poblacion_la_florida,CATEGORIA,-1,-1;NOM_CATEGO "NOM_CATEGO" true true false 255 Text 0 0,First,#,poblacion_la_florida,NOM_CATEGO,0,255;MANZENT_I "MANZENT_I" true true false 255 Text 0 0,First,#,poblacion_la_florida,MANZENT_I,0,255;TOTAL_PERS "TOTAL_PERS" true true false 4 Long 0 0,First,#,poblacion_la_florida,TOTAL_PERS,-1,-1;TOTAL_VIVI "TOTAL_VIVI" true true false 4 Long 0 0,First,#,poblacion_la_florida,TOTAL_VIVI,-1,-1;NHOMBRES "NHOMBRES" true true false 4 Long 0 0,First,#,poblacion_la_florida,NHOMBRES,-1,-1;NMUJERES "NMUJERES" true true false 4 Long 0 0,First,#,poblacion_la_florida,NMUJERES,-1,-1;Shape__Are "Shape__Are" true true false 8 Double 0 0,First,#,poblacion_la_florida,Shape__Are,-1,-1;Shape__Len "Shape__Len" true true false 8 Double 0 0,First,#,poblacion_la_florida,Shape__Len,-1,-1;COD_MANZ "COD_MANZ" true true false 8 Double 0 0,First,#,poblacion_la_florida,COD_MANZ,-1,-1')    
# Creación de definición de field calculator
# CALCULADORA(CAPA_DE_ENTRADA_QUE_SE_APLICA_CALCULO, NOMBRE_DEL_CAMPO_NUEVO)
def calculadora(layer, campo):
    arcpy.management.CalculateField(param9, campo,
                                    "densidad(!TOTAL_PERS!,!Shape__Are_1!,!JOIN_FID!)",
                                    "PYTHON3",
                                    """def densidad(poblacion,area,x):   
        if x == -1:
            den=0
            return den
        else:
            den=poblacion/area
            return den""", "DOUBLE", "NO_ENFORCE_DOMAINS")
    return
################################################################################################################
# LLAMAR A LAS DEFINICIONES
# Selección de las quebradas de la comuna
arcpy.AddMessage("Realizando selección de quebradas de la comuna")
select(param0, '1', param1, param2)
arcpy.AddMessage("Se han seleccionado las quebradas de la comuna")
# Generación de puntos a lo largo de las quebaradas de la comuna
arcpy.AddMessage("Generando puntos a lo largo de las quebradas de la comuna")
puntos(param2, param3)
arcpy.AddMessage("Se han generado los puntos a lo largo de las quebradas de la comuna")
# Generación de líneas aguas abajo de los puntos a lo largo de las quebradas
#arcpy.AddMessage("Generando líneas de aguas abajo")
#layer = traz_abajo(param3)
#arcpy.AddMessage("Se han generado las líneas aguas abajo")
# Generación de capa nueva de aguas abajo
#arcpy.AddMessage("Creando capa de aguas abajo")
#fcf(layer, param12,"aguas abajo")
#arcpy.AddMessage("Se ha creado la capa aguas abajo")
# Generación de buffers al rededor del trazado aguas abajo
distance = ["25 Meters",
           "50 Meters",
           "75 Meters"]
arcpy.AddMessage("Generando buffer a 25 metros")
buf(param11, param5, distance[0])
arcpy.AddMessage("Se ha realizo el buffer a 25 metros")
arcpy.AddMessage("Generando buffer a 50 metros")
buf(param11, param6, distance[1])
arcpy.AddMessage("Se ha realizo el buffer a 50 metros")
arcpy.AddMessage("Generando buffer a 75 metros")
buf(param11, param7, distance[2])
arcpy.AddMessage("Se ha realizo el buffer a 75 metros")
# Fusión de buffers
arcpy.AddMessage("Generando fusión de buffers de 25, 50 y 75 metros")
fusion(param5, param6, param7, param8)
arcpy.AddMessage("Se ha generado la fusión")
# Unión de manzanas con campos de población con buffer de trazado de aguas abajo
arcpy.AddMessage("Generando unión de manznas de La Florida y fusión de buffers")
join(param4,param8,param9)
arcpy.AddMessage("Se ha generado la unión")
# Unión de campos de la unión anterior y tabla de población
arcpy.AddMessage("Generando unión de tabla de población y unión realizada anteriormente")
union_camp(param9, param10, "COD_MANZ")
arcpy.AddMessage("Se ha unido la tabla al layer de unión")
# Cálculo de densidad para las manzanas
arcpy.AddMessage("Realizando cálculo de densidad poblacional afectada")
calculadora(param9,"poblacion_afectada")
arcpy.AddMessage("Se ha realizado el cálculo de densidad poblacional afectada")
