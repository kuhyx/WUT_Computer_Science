#ifndef GOOD_CPP
#define GOOD_CPP
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

Good::Good(): size_(DIMENSION), hazard(HAZARDS)
{
    size_ = {0, 0, 0};
    hazard = {0, 0, 0, 0};
    stateOfMatter = 0;
    weight = 0;
}

std::vector <int> Good::getSize_() const
{
    return size_;
}

std::vector <bool> Good::getHazard() const
{
    return hazard;
}

int Good::getStateOfMatter() const
{
    return stateOfMatter;
}

int Good::getWeight() const
{
    return weight;
}

void Good::setHazard(std::vector <bool> newHazard)
{
    hazard = newHazard;
}

void Good::setStateOfMatter(int newState)
{
    if(newState >= 0 && newState <= 2) stateOfMatter = newState;
    else std::cout << "newState must be a number between 0 and 2!" << std::endl;
}

void Good::setWeight(int newWeight)
{

    if(newWeight > 0) weight = newWeight;
}

void Good::setSize_(std::vector <int> newSize)
{
    if(newSize.size() > DIMENSION) return;
    for(int i = 0; i < DIMENSION; i++)
    {
        if(newSize[i] < 0) return;
    }
    size_ = newSize;
}

int Good::volume()
{
    return size_[0] * size_[1] * size_[2];
}

#endif // GOOD_CPP
