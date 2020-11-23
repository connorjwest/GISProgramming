# -*- coding: utf-8 -*-

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "GEOG676_Tools"
        self.alias = "GEOG676_Tools"

        # List of tool classes associated with this toolbox
        self.tools = [GraduatedColorsRenderer]


class GraduatedColorsRenderer(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Flood Map Renderer"
        self.description = "Render a map with graduated color"
        self.canRunInBackground = False # Only used in ArcMap
        self.category = "Rendering Tools"

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
        displayName="Input Layer",
        name="in_layer",
        datatype="GPFeatureLayer",
        parameterType="Required",
        direction="Input")

        param1 = arcpy.Parameter(
        displayName="Layer Join Field",
        name="join_layer",
        datatype="Field",
        parameterType="Required",
        direction="Input")
        param1.parameterDependencies = [param0.name]

        param2 = arcpy.Parameter(
        displayName="Input Table",
        name="in_table",
        datatype="DETable",
        parameterType="Required",
        direction="Input")

        param3 = arcpy.Parameter(
        displayName="Table Join Field",
        name="join_table",
        datatype="Field",
        parameterType="Required",
        direction="Input")
        param3.parameterDependencies = [param2.name]

        param4 = arcpy.Parameter(
            displayName="Classes number",
            name="ClassesNumber",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )
        param4.filter.type = "Range"
        param4.filter.list = [1, 100]

        param5 = arcpy.Parameter(
            displayName="Field using in classification",
            name="FieldClass",
            datatype="Field",
            parameterType="Required",
            direction="Input"
        )
        param5.parameterDependencies = [param2.name]

        params = [param0, param1, param2, param3, param4, param5]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):

        readTime = 2.5
        start = 0
        maximum = 100
        step = 25

        # Setup the progressor
        arcpy.SetProgressor("step", "Checking building proximity...", start, maximum, step)
        time.sleep(readTime)
        # Add message to the results pane
        arcpy.AddMessage("Rendering the Map...")


        project = arcpy.mp.ArcGISProject(r"C:/Users/xflyl/DevSource/Moxuan-Geog676/Project/" + r"\\GeoProgrammingProject.aprx")
        Counties_Layer = parameters[0].valueAsText
        Layer_Join_Field = parameters[1].valueAsText
        Input_Table = parameters[2].valueAsText
        Table_Join_Field = parameters[3].valueAsText
        Class_number_input = int(parameters[4].value)
        Classification_Field = parameters[5].valueAsText
        County_Event = "county_joined"
        
        County_joined_events = arcpy.AddJoin_management(Counties_Layer, Layer_Join_Field, 
                                                    Input_Table, Table_Join_Field)
        arcpy.CopyFeatures_management(County_joined_events, County_Event)

        counties = project.listMaps('Map')[0]

        for layer in counties.listLayers():
            # Check that the layer is a feature layer
            if layer.isFeatureLayer:
                # Obtain a copy of the layer's symbology
                symbology = layer.symbology
                # Makes sure symbology has an attribute "renderer"
                if hasattr(symbology, 'renderer'):
                    # Check if the layer's name is "Structures"
                    if layer.name == Counties_Layer:
                        symbology.updateRenderer('GraduatedColorsRenderer')
                        symbology.renderer.classificationField = Classification_Field
                        symbology.renderer.breakCount = Class_number_input
                        symbology.renderer.colorRamp = project.listColorRamps('Orange-Red (Continuous)')[0]
                        layer.symbology = symbology
                        arcpy.AddMessage("Renderer completed")
                    else:
                        arcpy.AddMessage("NOT Counties")
        project.saveACopy(r"C:/Users/xflyl/DevSource/Moxuan-Geog676/Project/" + r"\\floodmap_a.aprx")