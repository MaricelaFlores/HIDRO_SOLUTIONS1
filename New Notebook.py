import arcpy
gdb = r"D:\.Usach\Usach 2023\Dag\Trabajo semestral\hidroSol\hidroSol.gdb"
outDir = r"D:\.Usach\Usach 2023\Dag\Trabajo semestral\hidroSol\hidroSol.gdb\SALIDA"

puntos = "random_points"
fcReg = "region4"
num_pts = 700
dist_pts = "{} Meters".format(str(30))

arcpy.management.CreateRandomPoints(outDir, puntos, fcReg, "0 0 250 250", num_pts, dist_pts, "POINT", 0)

name = "poligonos"
outThie = outDir + "\\" + name

arcpy.analysis.CreateThiessenPolygons(puntos, outThie,"ONLY_FID")

name1 = "parcelas"
outParc = outDir + "\\" + name1

arcpy.analysis.Clip(outThie, fcReg, outParc, None)

eliminar = ["random_points", "poligonos"]
for i in eliminar:
    i_completo = outDir + "\\" + i
    arcpy.management.Delete(i_completo,"")

#se repite por lo que en la herramienta debe ser una función
#para humedad
mappings = arcpy.FieldMappings()
c_humedad = []
cId = "Id"
cVal = "gridcode"
c_humedad.append(cId)
c_humedad.append(cVal)

groupby = "{} MEAN".format(cVal)

variable = "humedad"
campos_variable = ["Input_FID"]
spacial_join = outDir + "\\" + "sp_humedad"

prom_campo = "MEAN_{}".format(cVal)

selType = "NEW SELECTION"

#Fieldmappings para los campos
for i in campos_variable:
    campo_parcelas = arcpy.FieldMap()
    campo_parcelas.addInputField(name1, i)
    mappings.addFieldMap(campo_parcelas)

for i in c_humedad:
    campo_humedad = arcpy.FieldMap()
    campo_humedad.addInputField(variable, i)
    mappings.addFieldMap(campo_humedad)

#spacialjoin entre parcelas y la variable
arcpy.analysis.SpatialJoin(name1, variable, spacial_join, "JOIN_ONE_TO_MANY", "KEEP_ALL", mappings, "INTERSECT")

#group by
outTemp_hum = gdb + "\\" + "tabTemp_hum"
arcpy.analysis.Statistics(spacial_join, outTemp_hum, groupby, campos_variable[0],"")

#unir a parcelas
arcpy.management.JoinField(name1, campos_variable[0], outTemp_hum, campos_variable[0], prom_campo,"NOT_USE_FM",None)

#donde sea nulo reemplazar con 0
arcpy.management.SelectLayerByAttribute(name1, selType , "{} IS NULL".format(prom_campo))
arcpy.management.CalculateField(name1, prom_campo, "0")
arcpy.management.SelectLayerByAttribute(name1, "CLEAR_SELECTION")

#eliminar tabla temporal
arcpy.management.Delete(outTemp_hum,"")

#para precipitacion
mappings = arcpy.FieldMappings()
c_prec = []
cId = "FID_"
cVal = "VALOR"
c_prec.append(cId)
c_prec.append(cVal)

groupby = "{} MEAN".format(cVal)

variable = "precipitacion"
campos_variable = ["Input_FID"]
spacial_join = outDir + "\\" + "sp_precipitacion"

prom_campo = "MEAN_{}".format(cVal)

#Fieldmappings para los campos
for i in campos_variable:
    campo_parcelas = arcpy.FieldMap()
    campo_parcelas.addInputField(name1, i)
    mappings.addFieldMap(campo_parcelas)

for i in c_prec:
    campo_prec = arcpy.FieldMap()
    campo_prec.addInputField(variable, i)
    mappings.addFieldMap(campo_prec)

#spacialjoin entre parcelas y la variable
arcpy.analysis.SpatialJoin(name1, variable, spacial_join, "JOIN_ONE_TO_MANY", "KEEP_ALL", mappings, "INTERSECT")

#group by
outTemp_hum = gdb + "\\" + "tabTemp_hum"
arcpy.analysis.Statistics(spacial_join, outTemp_hum, groupby, campos_variable[0],"")

#unir a parcelas
arcpy.management.JoinField(name1, campos_variable[0], outTemp_hum, campos_variable[0], prom_campo,"NOT_USE_FM",None)

#donde sea nulo reemplazar con 0
arcpy.management.SelectLayerByAttribute(name1, selType , "{} IS NULL".format(prom_campo))
arcpy.management.CalculateField(name1, prom_campo, "0")
arcpy.management.SelectLayerByAttribute(name1, "CLEAR_SELECTION")

#eliminar tabla temporal
arcpy.management.Delete(outTemp_hum,"")

#para temperatura
mappings = arcpy.FieldMappings()
c_tem = []
cId = "FID_"
cVal = "VALOR_T"
c_tem.append(cId)
c_tem.append(cVal)

groupby = "{} MEAN".format(cVal)

variable = "temperatura"
campos_variable = ["Input_FID"]
spacial_join = outDir + "\\" + "sp_temperatura"

prom_campo = "MEAN_{}".format(cVal)

#Fieldmappings para los campos
for i in campos_variable:
    campo_parcelas = arcpy.FieldMap()
    campo_parcelas.addInputField(name1, i)
    mappings.addFieldMap(campo_parcelas)

for i in c_tem:
    campo_temp = arcpy.FieldMap()
    campo_temp.addInputField(variable, i)
    mappings.addFieldMap(campo_temp)

#spacialjoin entre parcelas y la variable
arcpy.analysis.SpatialJoin(name1, variable, spacial_join, "JOIN_ONE_TO_MANY", "KEEP_ALL", mappings, "INTERSECT")

#group by
outTemp_hum = gdb + "\\" + "tabTemp_hum"
arcpy.analysis.Statistics(spacial_join, outTemp_hum, groupby, campos_variable[0],"")

#unir a parcelas
arcpy.management.JoinField(name1, campos_variable[0], outTemp_hum, campos_variable[0], prom_campo,"NOT_USE_FM",None)

#donde sea nulo reemplazar con 0
arcpy.management.SelectLayerByAttribute(name1, selType , "{} IS NULL".format(prom_campo))
arcpy.management.CalculateField(name1, prom_campo, "0")
arcpy.management.SelectLayerByAttribute(name1, "CLEAR_SELECTION")

#eliminar tabla temporal
arcpy.management.Delete(outTemp_hum,"")

#para evapo
mappings = arcpy.FieldMappings()
c_evapo = []
cId = "Id"
cVal = "gridcode_evap"
c_evapo.append(cId)
c_evapo.append(cVal)

groupby = "{} MEAN".format(cVal)

variable = "evapo"
campos_variable = ["Input_FID"]
spacial_join = outDir + "\\" + "sp_evapotranspiracion"

prom_campo = "MEAN_{}".format(cVal)

#Fieldmappings para los campos
for i in campos_variable:
    campo_parcelas = arcpy.FieldMap()
    campo_parcelas.addInputField(name1, i)
    mappings.addFieldMap(campo_parcelas)

for i in c_evapo:
    campo_evapo = arcpy.FieldMap()
    campo_evapo.addInputField(variable, i)
    mappings.addFieldMap(campo_evapo)

#spacialjoin entre parcelas y la variable
arcpy.analysis.SpatialJoin(name1, variable, spacial_join, "JOIN_ONE_TO_MANY", "KEEP_ALL", mappings, "INTERSECT")

#group by
outTemp_hum = gdb + "\\" + "tabTemp_hum"
arcpy.analysis.Statistics(spacial_join, outTemp_hum, groupby, campos_variable[0],"")

#unir a parcelas
arcpy.management.JoinField(name1, campos_variable[0], outTemp_hum, campos_variable[0], prom_campo,"NOT_USE_FM",None)

#donde sea nulo reemplazar con 0
arcpy.management.SelectLayerByAttribute(name1, selType , "{} IS NULL".format(prom_campo))
arcpy.management.CalculateField(name1, prom_campo, "0")
arcpy.management.SelectLayerByAttribute(name1, "CLEAR_SELECTION")

#eliminar tabla temporal
arcpy.management.Delete(outTemp_hum,"")

#no entra en la funcion
#para usos
mappings = arcpy.FieldMappings()
c_usos = []
cId = "ID"
cVal = "ID_USO"
c_usos.append(cId)
c_usos.append(cVal)

variable = "uso_1_2_3_4"
campos_variable = ["Input_FID"]
spacial_join = outDir + "\\" + "sp_usos"
outTemp = gdb + "\\" + "outTemp"

#Fieldmappings para los campos
for i in campos_variable:
    campo_parcelas = arcpy.FieldMap()
    campo_parcelas.addInputField(name1, i)
    mappings.addFieldMap(campo_parcelas)

for i in c_usos:
    campo_usos = arcpy.FieldMap()
    campo_usos.addInputField(variable, i)
    mappings.addFieldMap(campo_usos)

#spacialjoin entre parcelas y la variable
arcpy.analysis.SpatialJoin(name1, variable, spacial_join, "JOIN_ONE_TO_MANY", "KEEP_ALL", mappings, "INTERSECT")

#Frecuencia
arcpy.analysis.Frequency(spacial_join, outTemp, "{};{}".format(cVal, campos_variable[0]), cId)

#groupby
#crear tabla
outTemp1 = "outTemp1"
arcpy.management.CreateTable(gdb, outTemp1, outTemp)


# Crear una lista para almacenar los registros de la tabla de entrada
registros = []

# Utilizar un cursor de búsqueda para recorrer la tabla de entrada y obtener los registros
with arcpy.da.SearchCursor(outTemp, ["Input_FID", "ID_USO", "FREQUENCY"]) as cursor:
    ID_USO_mayor_FREQUENCY = {}
    
    for Input_FID, ID_USO, FREQUENCY in cursor:
        # Verificar si la Input_FID ya está en el diccionario y si el ID_USO actual tiene mayor FREQUENCY
        if Input_FID in ID_USO_mayor_FREQUENCY and FREQUENCY > ID_USO_mayor_FREQUENCY[Input_FID]["FREQUENCY"]:
            ID_USO_mayor_FREQUENCY[Input_FID] = {"ID_USO": ID_USO, "FREQUENCY": FREQUENCY}
        # Si la Input_FID no está en el diccionario, agregarla con el ID_USO y FREQUENCY actual
        elif Input_FID not in ID_USO_mayor_FREQUENCY:
            ID_USO_mayor_FREQUENCY[Input_FID] = {"ID_USO": ID_USO, "FREQUENCY": FREQUENCY}


# Utilizar un cursor de inserción para agregar los registros a la tabla de salida
with arcpy.da.InsertCursor(outTemp1, ["Input_FID", "ID_USO", "FREQUENCY"]) as cursor_insert:
    for Input_FID, info in ID_USO_mayor_FREQUENCY.items():
        cursor_insert.insertRow((Input_FID, info["ID_USO"], info["FREQUENCY"]))
    
#unir a parcelas
arcpy.management.JoinField(name1, campos_variable[0], outTemp1, campos_variable[0], cVal,"NOT_USE_FM",None)

#eliminar tabla temporal
eliminar = ["outTemp", "outTemp1"]
for i in eliminar:
    i_completo = gdb + "\\" + i
    arcpy.management.Delete(i_completo)

#eliminar shapes temporales
eliminar = ["sp_humedad", "sp_precipitacion", "sp_temperatura", "sp_evapotranspiracion", "sp_usos"]
for i in eliminar:
    i_completo = outDir + "\\" + i
    arcpy.management.Delete(i_completo)

#Valores

pond_hum = 0.07
pond_pp = 0.1
pond_tem = 0.21
pond_evapo = 0.15
pond_suelo = 0.47
tipo_suelo = [0.49, 0.35, 0.1, 0.06]

#agregar columna
campo_suelo = "suelo"
c_hum = "valor_humedad"
c_pp = "valor_precipitacion"
c_tem = "valor_temperatura"
c_ev = "valor_evapotranspiracion"
c_su = "valor_suelo"
campo_ev = "valor_evaluacion"
tyCampo = "DOUBLE"
cam_agregar = [campo_suelo, c_hum, c_pp, c_tem, c_ev, c_su, campo_ev]

for i in range(len(cam_agregar)):
    arcpy.management.AddField(name1, cam_agregar[i], tyCampo)

#cambiar el campo de suelo
camposc = ["ID_USO", "suelo"]
cursor = arcpy.da.UpdateCursor(name1, camposc)

for row in cursor:
    if (row[0] == "01"):
        row[1] = 0.49
    elif (row[0] == "02"):
        row[1] = 0.35
    elif (row[0] == "03"):
        row[1] = 0.1
    elif (row[0] == "04"):
        row[1] = 0.06
    else:
        row[1] = 0
    cursor.updateRow(row)

del cursor

#despues se crea una funcion para calcular el campo

#para humedad
campo1 = "MEAN_gridcode"
campo2 = "valor_humedad"

cursor = arcpy.UpdateCursor(name1)
for row in cursor:
    row.setValue(campo2, row.getValue(campo1) * pond_hum)
    cursor.updateRow(row)

#para precipitacion
campo1 = "MEAN_VALOR"
campo2 = "valor_precipitacion"

cursor = arcpy.UpdateCursor(name1)
for row in cursor:
    row.setValue(campo2, row.getValue(campo1) * pond_pp)
    cursor.updateRow(row)

#para temperatura
campo1 = "MEAN_VALOR_T"
campo2 = "valor_temperatura"

cursor = arcpy.UpdateCursor(name1)
for row in cursor:
    row.setValue(campo2, row.getValue(campo1) * pond_tem)
    cursor.updateRow(row)

#para evapotranspiracion
campo1 = "MEAN_gridcode_evap"
campo2 = "valor_evapotranspiracion"

cursor = arcpy.UpdateCursor(name1)
for row in cursor:
    row.setValue(campo2, row.getValue(campo1) * pond_evapo)
    cursor.updateRow(row)

#para suelo
campo1 = "suelo"
campo2 = "valor_suelo"

cursor = arcpy.UpdateCursor(name1)
for row in cursor:
    row.setValue(campo2, row.getValue(campo1) * pond_suelo)
    cursor.updateRow(row)

campo1 = "valor_humedad"
campo2 = "valor_evaluacion"
campo3 = "valor_precipitacion"
campo4 = "valor_temperatura"
campo5 = "valor_evapotranspiracion"
campo6 = "valor_suelo"

cursor = arcpy.UpdateCursor(name1)
for row in cursor:
    row.setValue(campo2, row.getValue(campo1) +row.getValue(campo3) +row.getValue(campo4) +row.getValue(campo5) +row.getValue(campo6)) 
    cursor.updateRow(row)

arcpy.ImportToolbox(r"D:\.Usach\Usach 2023\Dag\Trabajo semestral\hidroSol\hidroSol.gdb\hidroSol")
arcpy.NewToolbox.Evaluacion(
    predio=r"D:\.Usach\Usach 2023\Dag\Trabajo semestral\hidroSol\hidroSol.gdb\SALIDA\parcelas",
    id_predio="Input_FID",
    own_predio="Shape_Area",
    humedad=r"D:\.Usach\Usach 2023\Dag\Trabajo semestral\hidroSol\hidroSol.gdb\OPERATIVAS\humedad",
    id_hum="Id",
    val_hum="gridcode",
    precipitacion=r"D:\.Usach\Usach 2023\Dag\Trabajo semestral\hidroSol\hidroSol.gdb\OPERATIVAS\precipitacion",
    id_pp="FID_",
    val_pp="VALOR",
    temperatura=r"D:\.Usach\Usach 2023\Dag\Trabajo semestral\hidroSol\hidroSol.gdb\OPERATIVAS\temperatura",
    id_tem="FID_",
    val_tem="VALOR_T",
    evapotranspiracion=r"D:\.Usach\Usach 2023\Dag\Trabajo semestral\hidroSol\hidroSol.gdb\OPERATIVAS\evapo",
    id_evapo="Id",
    val_evapo="girdcode_evap",
    outDir=r"D:\.Usach\Usach 2023\Dag\Trabajo semestral\hidroSol\hidroSol.gdb\SALIDA"
)
