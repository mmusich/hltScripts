from OnLine_HLT_FULL import cms,process

for pathName in process.paths_():
  path = process.paths_()[pathName]
  hasDSF, hasPixClus = False, False
#  print(pathName)
  for (type_i, label_i) in path.expandAndClone().directDependencies():
    if type_i != 'modules': continue    
#    print('  ', label_i)
    mod = getattr(process, label_i)
    if (not hasDSF) and mod.type_() == 'DetectorStateFilter':
      hasDSF = True
    if (not hasPixClus) and mod.type_() == 'SiPixelRawToDigi':
      hasPixClus = True
  if hasDSF and not hasPixClus:
    print(pathName)
