from dump0 import cms, process

for attr_i in [
  'psets_',
  'vpsets_',
  'es_prefers_',
  'es_producers_',
  'es_sources_',
  'services_',
#  'filters_',
#  'producers_',
#  'analyzers_',
  'outputModules_',
#  'tasks_',
#  'sequences_',
#  'paths_',
  'endpaths_',
  'finalpaths_',
]:
  obj_i = getattr(process, attr_i)()
  for iter_j in obj_i:
    delattr(process, iter_j)
