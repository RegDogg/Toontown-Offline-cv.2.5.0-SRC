# Embedded file name: toontown.coghq.CashbotMintEntrance_Action00
from toontown.coghq.SpecImports import *
GlobalEntities = {1000: {'type': 'levelMgr',
        'name': 'LevelMgr',
        'comment': '',
        'parentEntId': 0,
        'cogLevel': 0,
        'farPlaneDistance': 1500,
        'modelFilename': 'phase_10/models/cashbotHQ/ZONE03a',
        'wantDoors': 1},
 1001: {'type': 'editMgr',
        'name': 'EditMgr',
        'parentEntId': 0,
        'insertEntity': None,
        'removeEntity': None,
        'requestNewEntity': None,
        'requestSave': None},
 0: {'type': 'zone',
     'name': 'UberZone',
     'comment': '',
     'parentEntId': 0,
     'scale': 1,
     'description': '',
     'visibility': []},
 10000: {'type': 'entrancePoint',
         'name': '<unnamed>',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(0.0, 6.0, 0.0),
         'hpr': Vec3(0.0, 0.0, 0.0),
         'scale': 1,
         'entranceId': 0,
         'radius': 15,
         'theta': 20},
 10001: {'type': 'mintProduct',
         'name': '<unnamed>',
         'comment': '',
         'parentEntId': 10004,
         'pos': Point3(-11.4890069962, 20.1173057556, 0.0),
         'hpr': Point3(0.0, 0.0, 0.0),
         'scale': Vec3(1.0, 1.0, 1.0),
         'mintId': 12700},
 10003: {'type': 'mintProduct',
         'name': 'copy of <unnamed>',
         'comment': '',
         'parentEntId': 10004,
         'pos': Point3(-20.4286708832, 12.2706327438, 0.0),
         'hpr': Vec3(90.0, 0.0, 0.0),
         'scale': Vec3(1.0, 1.0, 1.0),
         'mintId': 12700},
 10007: {'type': 'mintProduct',
         'name': 'copy of <unnamed>',
         'comment': '',
         'parentEntId': 10004,
         'pos': Point3(-19.2144012451, 20.1173057556, 0.0),
         'hpr': Point3(0.0, 0.0, 0.0),
         'scale': Vec3(1.0, 1.0, 1.0),
         'mintId': 12700},
 10006: {'type': 'model',
         'name': 'crateStack',
         'comment': '',
         'parentEntId': 10002,
         'pos': Point3(10.5386743546, 18.1184597015, 0.0),
         'hpr': Vec3(270.0, 0.0, 0.0),
         'scale': Vec3(1.0, 1.0, 1.0),
         'collisionsOnly': 0,
         'flattenType': 'light',
         'loadType': 'loadModelCopy',
         'modelPath': 'phase_10/models/cashbotHQ/crates_G1'},
 10008: {'type': 'model',
         'name': '<unnamed>',
         'comment': '',
         'parentEntId': 10002,
         'pos': Point3(13.8522205353, -20.3127307892, 0.0),
         'hpr': Vec3(0.0, 0.0, 0.0),
         'scale': Vec3(1.0, 1.0, 1.0),
         'collisionsOnly': 0,
         'flattenType': 'light',
         'loadType': 'loadModelCopy',
         'modelPath': 'phase_10/models/cashbotHQ/crates_C1'},
 10002: {'type': 'nodepath',
         'name': 'props',
         'comment': '',
         'parentEntId': 0,
         'pos': Point3(0.0, 0.0, 0.0),
         'hpr': Vec3(0.0, 0.0, 0.0),
         'scale': 1},
 10004: {'type': 'nodepath',
         'name': 'product',
         'comment': '',
         'parentEntId': 10002,
         'pos': Point3(0.0, 0.0, 0.0),
         'hpr': Vec3(0.0, 0.0, 0.0),
         'scale': Vec3(1.0, 1.0, 1.0)}}
Scenario0 = {}
levelSpec = {'globalEntities': GlobalEntities,
 'scenarios': [Scenario0]}