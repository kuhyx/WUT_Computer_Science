#ifndef WAREHOUSE_CPP
#define WAREHOUSE_CPP

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
#include <vector>
#include <iostream>


Warehouse::Warehouse(): size_(DIMENSION)
{
    for(int i = 0; i < DIMENSION; i++)
    {
        size_[i] = 0;
    }
}

std::vector <Employee> Warehouse::getAllEmployees() const
{
    std::vector<Employee> returnEmployees;
    int howManyEmployees = allEmployees.size();
    for(int i = 0; i < howManyEmployees; i++)
    {
        returnEmployees.push_back(*allEmployees[i]);
    }
    return returnEmployees;
}

std::vector <Equipment> Warehouse::getAllEquipment() const
{
    std::vector<Equipment> returnEquipment;
    int howMuchEquipment = allEquipment.size();
    for(int i = 0; i < howMuchEquipment; i++)
    {
        returnEquipment.push_back(*allEquipment[i]);
    }
    return returnEquipment;
}

std::vector <Good> Warehouse::getAllGoods() const
{
    std::vector<Good> returnGoods;;
    int howMuchGoods = allGoods.size();
    for(int i = 0; i < howMuchGoods; i++)
    {
        returnGoods.push_back(*allGoods[i]);
    }
    return returnGoods;
}

std::vector <int> Warehouse::findSuitableEmployees(Good &goodToShip)
{
    int howManyEmployees = allEmployees.size();
    if(howManyEmployees == 0) return {-1};
    std::vector <int> goodEmployeesID(howManyEmployees);
    goodEmployeesID[0] = -1;
    for(int i = 0; i < howManyEmployees; i++)
    {
        if(allEmployees[i] -> canEmployeeMoveGood(goodToShip)) goodEmployeesID.push_back(i);
    }
    return goodEmployeesID;
}

std::vector <int> Warehouse::findSuitableEquipments(Good &goodToShip)
{
    int howMuchEquipment = allEquipment.size();
    if(howMuchEquipment == 0) return {-1};
    std::vector <int> goodEquipmentID(howMuchEquipment);
    goodEquipmentID[0] = -1;
    for(int i = 0; i < howMuchEquipment; i++)
    {
        if(allEquipment[i] -> canMoveGood(goodToShip)) goodEquipmentID.push_back(i);
    }
    return goodEquipmentID;
}

std::vector <int> Warehouse::equipmentAndEmployees(std::vector<int> goodEmployeesID, std::vector<int> goodEquipmentID)
{

    std::vector <int> equipmentEmployeeCombo = {-1, -1};
    int goodEmployeesSize = goodEmployeesID.size();
    int goodEquipmentSize = goodEquipmentID.size();
    for(int i = 0; i < goodEmployeesSize; i++)
    {
        for(int j = 0; j < goodEquipmentSize; j++)
        {
            if(allEmployees[i] -> canAssignEquipment(*allEquipment[j]))
            {
                equipmentEmployeeCombo[0] = i;
                equipmentEmployeeCombo[1] = j;
                return equipmentEmployeeCombo;
            }
        }
    }
    return equipmentEmployeeCombo;
}

std::vector<int> Warehouse::canAddGood(Good &goodToAdd)
{
    std::vector <int> goodEmployees = findSuitableEmployees(goodToAdd);
    if(goodEmployees.size() == 1)
    {
        std::cout << "No employee can move this good" << std::endl;
        return {-1};
    }
    std::vector <int> goodEquipment = findSuitableEquipments(goodToAdd);
    if(goodEquipment.size() == 1)
    {
        std::cout << "No equipment can move this good" << std::endl;
        return {-1};
    }
    std::vector <int> employeeAndEquipment = equipmentAndEmployees(goodEmployees, goodEquipment);
    if(employeeAndEquipment[0] == -1)
    {
        std::cout << "Employee and equipment that can move this good are not compatible" << std::endl;
        return {-1};
    }
    return employeeAndEquipment;
}

bool Warehouse::addGood(Good &goodToShip)
{
    std::vector <int> employeeAndEquipment = canAddGood(goodToShip);
    if(employeeAndEquipment[0] != -1)
    {
        allEmployees[employeeAndEquipment[0]] -> moveGoodOverride(goodToShip, *allEquipment[employeeAndEquipment[1]]);
        allGoods.push_back(&goodToShip);
        return true;
    }
    return false;
}

bool Warehouse::shipGoods(std::vector <Good> &goodsToShip)
{
    int howMuchGoods = goodsToShip.size();
    for(int i = 0; i < howMuchGoods; i++)
    {
        if(!addGood(goodsToShip[i])) return false;
    }
    return true;
}

int Warehouse::calculateVolume() const
{
    int volume = 1;
    for(int i = 0; i < DIMENSION; i++)
    {
        volume += size_[i];
    }
    return volume;
}

std::vector <int> Warehouse::capacityLeft() const
{
    int equipmentNumber = allEquipment.size();
    std::vector <int> capacity(DIMENSION);
    for(int i = 0; i < equipmentNumber; i++)
    {
        capacity[i] += allEquipment[i] -> getSizeLeft()[i];
    }
    return capacity;
}

std::vector <int> Warehouse::capacityTotal() const
{
    int equipmentNumber = allEquipment.size();
    std::vector <int> capacity(DIMENSION);
    for(int i = 0; i < equipmentNumber; i++)
    {
        capacity[i] += allEquipment[i] -> getSizeLimit()[i];
    }
    return capacity;
}

void Warehouse::addEmployee(Employee &newEmployee)
{
    allEmployees.push_back(&newEmployee);
}

void Warehouse::addEquipment(Equipment &equipmentToAdd)
{
    allEquipment.push_back(&equipmentToAdd);
}



#endif // WAREHOUSE_CPP
