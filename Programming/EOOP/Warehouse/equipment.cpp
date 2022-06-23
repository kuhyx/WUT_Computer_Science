#ifndef EQUIPMENT_CPP
#define EQUIPMENT_CPP
#include "employee.hpp"
#include "equipment.hpp"
#include "good.hpp"
#include "warehouse.hpp"

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

#include <iostream>

Equipment::Equipment(): canTransportHazard(HAZARDS), canTransportState(STATE), sizeLimit(DIMENSION), sizeLeft(DIMENSION), trainingRequired(CERTIFICATES)
{
    for(int i = 0; i < HAZARDS; i++)
    {
        canTransportHazard[i] = 0;
    }

    for(int i = 0; i < STATE; i++)
    {
        canTransportState[i] = 0;
    }

    for(int i = 0; i < DIMENSION; i++)
    {
        sizeLimit[i] = 0;
    }

    sizeLeft = sizeLimit;

    for(int i = 0; i < CERTIFICATES; i++)
    {
        trainingRequired[i] = 0;
    }

    timesUsed = 0;
    timesUsedLimit = 0;
    weightLimit = 0;
    weightLeft = 0;
}

std::vector<bool> Equipment::getCanTranportHazard() const
{
    return canTransportHazard;
}

void Equipment::setCanTransportHazard(std::vector <bool> newHazard)
{
    canTransportHazard = newHazard;
}

std::vector<bool> Equipment::getCanTransportState() const
{
    return canTransportState;
}

void Equipment::setCanTransportState(std::vector <bool> newState)
{
    canTransportState = newState;
}

std::vector<int> Equipment::getSizeLimit() const
{
    return sizeLimit;
}

void Equipment::setSizeLimit(std::vector<int> newSize)
{
    for(int i = 0; i < DIMENSION; i++)
    {
        if(newSize[i] >= 0)
        {
            int sizeOccupied = sizeLimit[i] - sizeLeft[i];
            sizeLeft[i] = newSize[i] - sizeOccupied;
            sizeLimit[i] = newSize[i];
        }
    }
}

std::vector<int> Equipment::getSizeLeft() const
{
    return sizeLeft;
}

void Equipment::setSizeLeft(std::vector<int> newSizeLeft)
{
    for(int i = 0; i < DIMENSION; i++)
    {
        if(newSizeLeft[i] >= 0 && newSizeLeft <= sizeLimit) sizeLeft[i] = newSizeLeft[i];
    }
}

void Equipment::occupySpaceGood(Good &someGood)
{
    std::vector<int> goodSize = someGood.getSize_();
    for(int i = 0; i < DIMENSION; i++)
    {
        if(goodSize[i] <= sizeLeft[i]) sizeLeft[i] -= goodSize[i];
    }
}

int Equipment::getTimesUsed() const
{
    return timesUsed;
}

void Equipment::setTimesUsed(int newTimesUsed)
{
    if(newTimesUsed >= 0) timesUsed = newTimesUsed;
}

int Equipment::getTimesUsedLimit() const
{
    return timesUsedLimit;
}

void Equipment::setTimesUsedLimit(int newTimesUsedLimit)
{
    if(newTimesUsedLimit >= 0) timesUsedLimit = newTimesUsedLimit;
}

std::vector<bool> Equipment::getTrainingRequired() const
{
    return trainingRequired;
}

void Equipment::setTrainingRequired(int trainingNumber)
{
    if(trainingNumber >= 0 && trainingNumber <= CERTIFICATES - 1) trainingRequired[trainingNumber] = 1;
}

int Equipment::getWeightLimit() const
{
    return weightLimit;
}

void Equipment::setWeightLimit(int newWeightLimit)
{
    if(newWeightLimit >= 0) weightLimit = newWeightLimit;
}

int Equipment::getWeightLeft() const
{
    return weightLeft;
}

void Equipment::setWeightLeft(int newWeightLeft)
{
    if(newWeightLeft >= 0) weightLeft = newWeightLeft;
}



bool Equipment::canMoveHazard(Good &someGood)
{
    std::vector <bool> Hazard = someGood.getHazard();
    for(int i = 0; i < HAZARDS; i++)
    {
        if(canTransportHazard[i] == 0 && Hazard[i] == 1) return 0;
    }
    return 1;
}

bool Equipment::canMoveState(Good &someGood)
{
    if(canTransportState[someGood.getStateOfMatter()]) return true;
    return false;
}

bool Equipment::canMoveSize(Good &someGood)
{
    std::vector <int> goodSize = someGood.getSize_();
    for(int i = 0; i < DIMENSION; i++)
    {
        if(sizeLimit[i] < goodSize[i]) return false;
    }
    return true;
}

bool Equipment::needsRepair() const
{
    if(timesUsed > timesUsedLimit) return true;
    return false;
}

bool Equipment::canMoveGood(Good &someGood)
{
    if(!canMoveHazard(someGood))
    {
        std::cout << "This equipment cannot move good with this hazard" << std::endl;
        return false;
    }
    if(!canMoveState(someGood))
    {
        std::cout << "This equipment cannot move good with this state" << std::endl;
        return false;
    }
    if(!canMoveSize(someGood))
    {
        std::cout << "This equipment cannot move good of this size" << std::endl;
        return false;
    }
    if(needsRepair())
    {
        std::cout << "This equipment needs repair" << std::endl;
        return false;
    }
    if(someGood.getWeight() > getWeightLeft())
    {
        std::cout << "This good is too heavy to be moved by this equipment" << std::endl;
    }
    return true;
}

int Equipment::volumeLimit() const
{
    int volume = 1;
    for(int i = 0; i < DIMENSION; i++)
    {
        volume *= sizeLimit[i];
    }
    return volume;
}

int Equipment::volumeLeft() const
{
    int volume = 1;
    for(int i = 0; i < DIMENSION; i++)
    {
        volume *= sizeLeft[i];
    }
    return volume;
}

void Equipment::operator = (Equipment const &otherEquipment)
{
    this -> canTransportHazard = otherEquipment.getCanTranportHazard();
    this -> canTransportState = otherEquipment.getCanTransportState();
    this -> sizeLimit = otherEquipment.getSizeLimit();
    this -> timesUsed = otherEquipment.getTimesUsed();
    this -> timesUsedLimit = otherEquipment.getTimesUsedLimit();
    this -> trainingRequired = otherEquipment.getTrainingRequired();
}





#endif // EQUIPMENT_CPP
