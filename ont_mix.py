from owlready2 import *

onto = get_ontology("bridge.rdf").load()


def healthiest_component():
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
    components_with_condition_index = []
    print(onto.Component.instances())
    for component in onto.Component.instances():
        if hasattr(component, 'has_condition_index'):
            condition_index = component.has_condition_index
            if condition_index:
                components_with_condition_index.append((component, max(condition_index)))

    if components_with_condition_index:
        max_condition_index = max([c_index for _, c_index in components_with_condition_index])

        healthiest_components = [component for component, c_index in components_with_condition_index if
                                 c_index == max_condition_index]
        print(f"Highest Condition Index: {max_condition_index}")
        print("Defects with the highest severity level:")
        for component in healthiest_components:
            print(str(component).split(".")[1])

    else:
        print("No defects with severity levels found.")


def most_compromised_component():
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
    components_with_condition_index = []
    print(onto.Component.instances())
    for component in onto.Component.instances():
        if hasattr(component, 'has_condition_index'):
            condition_index = component.has_condition_index
            if condition_index:
                components_with_condition_index.append((component, max(condition_index)))

    if components_with_condition_index:
        min_condition_index = min([c_index for _, c_index in components_with_condition_index])

        most_compromised_components = [component for component, c_index in components_with_condition_index if
                                       c_index == min_condition_index]
        print(f"Highest Severity Level: {min_condition_index}")
        print("Defects with the highest severity level:")
        for component in most_compromised_components:
            print(str(component).split(".")[1])

    else:
        print("No defects with severity levels found.")


def highest_severity_defect():
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
    defects_with_severity = []
    for defect in onto.Defect.instances():
        if hasattr(defect, 'has_severity_level'):
            severity_levels = defect.has_severity_level
            if severity_levels:
                defects_with_severity.append((defect, max(severity_levels)))

    if defects_with_severity:
        max_severity_level = max([severity for _, severity in defects_with_severity])

        most_severe_defects = [defect for defect, severity in defects_with_severity if severity == max_severity_level]
        print(f"Highest Severity Level: {max_severity_level}")
        print("Defects with the highest severity level:")
        for defect in most_severe_defects:
            print(str(defect).split(".")[1])

    else:
        print("No defects with severity levels found.")


with onto:
    class Component(Thing):
        def component_material(self):
            sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
            search_item = str(self).split(".")[1]
            specific_component = onto.search_one(iri=f"*{search_item}")
            if specific_component:
                # Retrieve the severity level of the specific defect
                material = specific_component.has_material
                # Print the severity level
                print(f"Material of {specific_component.name} is: {material[0].name}")
            else:
                print("Something went wrong")

        def defects_on_material(self):
            sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
            search_item = str(self).split(".")[1]
            specific_component = onto.search_one(iri=f"*{search_item}")
            if specific_component:
                # Retrieve the severity level of the specific defect
                defects = specific_component.has_defect
                # Print the severity level
                print(f"Defects on {specific_component.name} are: {defects}")
            else:
                print("Something went wrong")

        def assign_component_condition_index(self):
            sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
            search_item = str(self).split(".")[1]
            specific_component = onto.search_one(iri=f"*{search_item}")
            condition_index = 100
            if specific_component:
                # Retrieve the severity level of the specific defect
                defects = specific_component.has_defect
                is_minus = False
                for defect in defects:
                    severity_level = defect.has_severity_level
                    print(defect.is_a)
                    if defect.is_a[0] == onto.Exposedbar or defect.is_a[0] == onto.Spallation or defect.is_a[
                        0] == onto.Efflorescence:
                        is_minus = True
                    if severity_level:
                        condition_index -= int(severity_level[0])
                if is_minus:
                    condition_index -= 15
                specific_component.has_condition_index = [condition_index]
                # Print the severity level
                print(f"Condition index {specific_component.has_condition_index}")
                print(f"Successfully updated")
                onto.save(file="bridge.rdf", format="rdfxml")
            else:
                print("Specific defect not found.")

        def assign_component_condition_state(self):

            sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
            search_item = str(self).split(".")[1]
            specific_component = onto.search_one(iri=f"*{search_item}")

            if specific_component:
                # Retrieve the severity level of the specific defect
                condition_index = int(specific_component.has_condition_index[0])
                print(condition_index)
                if condition_index:
                    if condition_index >= 90:
                        good = onto.search_one(iri="*Good")
                        specific_component.has_condition_state = [good]
                    elif condition_index < 90 and condition_index > 75:
                        fair = onto.search_one(iri="*Fair")
                        specific_component.has_condition_state = [fair]
                    elif condition_index <= 75 and condition_index > 55:
                        bad = onto.search_one(iri="*Bad")
                        print(bad)
                        specific_component.has_condition_state = [bad]
                    elif condition_index <= 55:
                        critical = onto.search_one(iri="*Critical")
                        specific_component.has_condition_state = [critical]
                # Print the severity level
                print(f"Severity level of {specific_component.has_condition_index}")
                print(f"Severity level of {specific_component.has_condition_state}")
                onto.save(file="bridge.rdf", format="rdfxml")
            else:
                print("has no condition index please assign one")

    class Defect(Thing):
        def severity_level_of_defect(self):
            sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
            search_item = str(self).split(".")[1]
            specific_defect = onto.search_one(iri=f"*{search_item}")
            if specific_defect:
                # Retrieve the severity level of the specific defect
                severity_level = specific_defect.has_severity_level

                # Print the severity level
                print(f"Severity level of {specific_defect.name}: {severity_level[0]}")
            else:
                print("Specific defect not found.")

        def defect_material_type(self):
            sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
            search_item = str(self).split(".")[1]
            specific_defect = onto.search_one(iri=f"*{search_item}")
            if specific_defect:
                # Retrieve the severity level of the specific defect
                material = specific_defect.material_located_on

                # Print the severity level
                print(f"Severity level of {specific_defect.name}: {material[0]}")
            else:
                print("Specific defect not found.")

        def severity_of_defect(self):
            sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
            search_item = str(self).split(".")[1]
            specific_defect = onto.search_one(iri=f"*{search_item}")
            if specific_defect:
                # Retrieve the severity level of the specific defect
                severity_level = specific_defect.has_severity

                # Print the severity level
                print(f"Severity level of {specific_defect.name}: {severity_level[0]}")
            else:
                print("Specific defect not found.")


my_comp = Component("ReinforcedConcreteApproachSlab5")
my_comp.assign_component_condition_index()
my_comp.assign_component_condition_state()
