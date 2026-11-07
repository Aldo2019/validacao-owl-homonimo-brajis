import os, platform, subprocess, owlready2
from owlready2 import get_ontology, sync_reasoner_hermit, OwlReadyInconsistentOntologyError, World

def carregar(arquivo):
    w = World()
    return w, w.get_ontology("file://" + os.path.abspath(arquivo)).load()

print("Python:", platform.python_version(), "| owlready2:", owlready2.VERSION)
print(subprocess.run(["java", "-version"], capture_output=True, text=True).stderr.splitlines()[0])

print("\n=== CENÁRIO A (com axioma 5) ===")
w, onto = carregar("cenario_A_com_distincao.owl")
try:
    with onto:
        sync_reasoner_hermit(w)
    print("Resultado: CONSISTENTE (inesperado)")
except OwlReadyInconsistentOntologyError:
    print("Resultado: INCONSISTENTE (esperado)")

print("\n=== CENÁRIO B (sem axioma 5) ===")
w, onto = carregar("cenario_B_sem_distincao.owl")
with onto:
    sync_reasoner_hermit(w, infer_property_values=True)
print("Resultado: CONSISTENTE")
leao = onto.search_one(iri="*leaoXIV")
rob = onto.search_one(iri="*robertWPrevost")
print("Indivíduos inferidos como idênticos a leaoXIV:", list(leao.equivalent_to))
print("leaoXIV sameAs robertWPrevost inferido?", rob in leao.equivalent_to)

print("\n=== CENÁRIO B – consulta: quem é o mesmo indivíduo que robertWPrevost? ===")
from owlready2 import Thing, OneOf
w, onto = carregar("cenario_B_sem_distincao.owl")
leao = onto.search_one(iri="*leaoXIV")
rob = onto.search_one(iri="*robertWPrevost")
with onto:
    class MesmoQueRobert(Thing):
        equivalent_to = [OneOf([rob])]
    sync_reasoner_hermit(w)
print("Instâncias inferidas de {robertWPrevost}:", list(MesmoQueRobert.instances()))
print("leaoXIV inferido idêntico a robertWPrevost?", leao in MesmoQueRobert.instances())


