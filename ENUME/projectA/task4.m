function [eigenValuesNoShifts, iterationsNoShifts, finalMatrixNoShifts, eigenValuesShifts, iterationsShifts, finalMatrixShifts] = task4(Matrix)
    [eigenValuesNoShifts, iterationsNoShifts, finalMatrixNoShifts] = QRNoShifts(Matrix);
    [eigenValuesShifts, iterationsShifts, finalMatrixShifts] = QRShifts(Matrix);
end