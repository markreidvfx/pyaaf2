from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
import unittest
import aaf2
import common
import uuid


class DictionaryTests(unittest.TestCase):

    def test_operationdef(self):

        result_file = common.get_test_file('operation_def.aaf')

        parm_id = uuid.uuid4()
        effect_id = uuid.uuid4()

        with aaf2.open(result_file, 'w') as f:

            typedef = f.dictionary.lookup_typedef("Rational")
            param = f.create.ParameterDef(parm_id, "AvidEffectID", "avid effect id", typedef)
            f.dictionary.register_def(param)

            op_def = f.create.OperationDef(effect_id, "MatteKey_2", "matte key def")
            op_def.media_kind = "Picture"
            f.dictionary.register_def(op_def)
            op_def['IsTimeWarp'].value = False
            op_def['Bypass'].value = 2
            op_def['NumberInputs'].value = 3
            op_def['OperationCategory'].value = "OperationCategory_Effect"
            op_def['ParametersDefined'].append(param)

            length = 100
            operation = f.create.OperationGroup(op_def, length)

            mob = f.create.MasterMob()
            f.content.mobs.append(mob)
            slot = mob.create_picture_slot()
            slot.segment.components.append(operation)

        with aaf2.open(result_file, 'r') as f:
            param = f.dictionary.lookup_parameterdef('AvidEffectID')
            assert param.auid == parm_id

            op_def = f.dictionary.lookup_operationdef("MatteKey_2")
            assert op_def.auid == effect_id
            assert op_def.media_kind == 'Picture'
            assert op_def['IsTimeWarp'].value == False
            assert op_def['Bypass'].value == 2
            assert op_def['NumberInputs'].value == 3
            assert op_def['OperationCategory'].value == "OperationCategory_Effect"

            assert param in op_def['ParametersDefined'].value

            mob = next(f.content.mobs.values())
            slot = mob.slots.value[0]
            op = slot.segment.components.value[0]
            assert op.operation == op_def

if __name__ == "__main__":
    unittest.main()
