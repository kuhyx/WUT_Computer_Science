#ifndef EMPLOYEE_CPP
#define EMPLOYEE_CPP

#ifndef DIMENSION
#define DIMENSION 3
#endif // DIMENSION

#ifndef HAZARDS
#define HAZARDS 3
#endif // HAZARDS

#ifndef STATE
#define STATE 3
#endif // STATE

#ifndef CERTIFICATES
#define CERTIFICATES 10
#endif // CERTIFICATES

#include "employee.hpp"
#include "equipment.hpp"
#include "good.hpp"
#include "warehouse.hpp"
#include <iostream>

Employee::Employee(): equipmentTraining(CERTIFICATES), hazardTraining(HAZARDS),
                      statesTraining(STATE)
{
    for(int i = 0; i < CERTIFICATES; i++)
    {
        equipmentTraining[i] = 0;
    }

    for(int i = 0; i < HAZARDS; i++)
    {
        hazardTraining[i] = 0;
    }

    for(int i = 0; i < STATE; i++)
    {
        statesTraining[i] = 0;
    }

    canRepair = 0;

    Equipment assignedEquipment;
}

std::vector <bool> Employee::getEquipmentTraining() const
{
    return equipmentTraining;
}

std::vector <bool> Employee::getHazardTraining() const
{
    return hazardTraining;
}

std::vector <bool> Employee::getStatesTraining() const
{
    return statesTraining;
}

Equipment Employee::getAssignedEquipment() const
{
    return assignedEquipment;
}

bool Employee::getCanRepair() const
{
    return canRepair;
}

void Employee::trainEquipment(int certificateNumber)
{
    if(certificateNumber >= 0 && certificateNumber <= CERTIFICATES - 1)
    {
        equipmentTraining[certificateNumber] = 1;
    }
}

void Employee::trainHazard(int certificateNumber)
{
    if(certificateNumber >= 0 && certificateNumber <= HAZARDS - 1)
    {
        hazardTraining[certificateNumber] = 1;
    }
}

void Employee::trainStates(int certificateNumber)
{
    if(certificateNumber >= 0 && certificateNumber <= STATE - 1)
    {
        statesTraining[certificateNumber] = 1;
    }
}

void Employee::trainRepair()
{
    canRepair = 1;
}

bool Employee::canAssignEquipment(Equipment toBeAssigned) const
{
    std::vector <bool> trainingNeeded = toBeAssigned.getTrainingRequired();
    for(int i = 0; i < CERTIFICATES - 1; i++)
    {
        if((equipmentTraining[i] == 0) && (trainingNeeded[i] == 1)) return false;
    }
    return true;
}

void Employee::assignEquipment(Equipment &newEquipment)
{
    if(canAssignEquipment(newEquipment)) assignedEquipment = newEquipment;
}

void Employee::removeEquipment()
{
    Equipment emptyEquipment;
    assignedEquipment = emptyEquipment;
}

bool Employee::canEmployeeMoveGoodState(Good &goodToMove) const
{
    int goodState = goodToMove.getStateOfMatter();
    return statesTraining[goodState];
}

bool Employee::canEmployeeMoveGoodHazard(Good &goodToMove) const
{
    std::vector <bool> goodHazard = goodToMove.getHazard();
    for(int i = 0; i < HAZARDS; i++)
    {
        if(hazardTraining[i] == 0 && goodHazard[i] == 1) return false;
    }
    return true;
}

bool Employee::canEmployeeMoveGood(Good &goodToMove) const
{
    if(!canEmployeeMoveGoodState(goodToMove))
    {
        std::cout << "Employee can't move the state of this good" << std::endl;
        return false;
    }
    if(!canEmployeeMoveGoodHazard(goodToMove))
    {
        std::cout << "Employee can't move the hazards of this good" << std::endl;
        return false;
    }
    return true;
}

bool Employee::canMoveGood(Good &goodToMove, Equipment &toWhichMove, Equipment &fromWhichMove) const
{
    if(!toWhichMove.canMoveGood(goodToMove))
    {
        std::cout << "Equipment toWhichWeMove cannot hold this good" << std::endl;
        return false;
    }
    if(!fromWhichMove.canMoveGood(goodToMove))
    {
        std::cout << "Equipment fromWhichMove cannot move this good" << std::endl;
        return false;
    }
    if(!canEmployeeMoveGood(goodToMove))
    {
        std::cout << "Employee cannot move this good" << std::endl;
        return false;
    }
    if(!canAssignEquipment(fromWhichMove))
    {
        std::cout << "Employee cannot be assigned equipment fromWhichMove" << std::endl;
        return false;
    }
    return true;
}

bool Employee::moveGood(Good &goodToMove, Equipment &toWhichMove, Equipment &fromWhichMove) const
{
    if(canMoveGood(goodToMove, toWhichMove, fromWhichMove))
    {
        toWhichMove.setTimesUsed(toWhichMove.getTimesUsed() + 1);
        fromWhichMove.setTimesUsed(fromWhichMove.getTimesUsed() + 1);
        toWhichMove.occupySpaceGood(goodToMove);
        return true;
    }
    return false;
}

void Employee::moveGoodOverride(Good &goodToMove, Equipment &toWhichMove) const
{
    toWhichMove.setTimesUsed(toWhichMove.getTimesUsed() + 1);
    toWhichMove.occupySpaceGood(goodToMove);
}

bool Employee::repairEquipment(Equipment &toRepair) const
{
    if(getCanRepair() && toRepair.needsRepair())
    {
        toRepair.setTimesUsed(0);
        return true;
    }
    return false;
}

#endif // EMPLOYE_CPP
