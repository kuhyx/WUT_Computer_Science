#include <iostream>
#include "employee.hpp"
#include "equipment.hpp"
#include "good.hpp"
#include "warehouse.hpp"
#include "employee.cpp"
#include "equipment.cpp"
#include "good.cpp"
#include "warehouse.cpp"
#include <vector>
#include <iostream>

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

void error_message(const std::string& message)
{
    std::cerr << "Error - " << message << "!" << std::endl;
}


void print(std::string s)
{
    std::cout << s << std::endl;
}


void printIntVector(std::vector<int> v)  // v stands for vector
{
    for(unsigned int i = 0; i < v.size(); i++)
    {
        std::cout << "vector[" << i << "] = " << v[i] << "; ";
    }
    std::cout << std::endl;
}

void printBoolVector(std::vector<bool> v)
{
    for(unsigned int i = 0; i < v.size(); i++)
    {
        std::cout << "vector[" << i << "] = " << v[i] << "; ";
    }
    std::cout << std::endl;
}

void printFullInfoGood(Good goodInfo)
{
    print("Good info: ");
    print("Hazards: ");
    printBoolVector(goodInfo.getHazard());
    print("Size: ");
    printIntVector(goodInfo.getSize_());
    print("State of matter: ");
    std::cout << goodInfo.getStateOfMatter() << std::endl;
    print("Weight: ");
    std::cout << goodInfo.getWeight() << std::endl;
}


void printFullInfoEquipment(Equipment equipmentInfo)
{
    print("Equipment info: ");
    print("Size limit: ");
    printIntVector(equipmentInfo.getSizeLimit());
    print("Can Transport State: ");
    printBoolVector(equipmentInfo.getCanTransportState());
    print("Can Transport Hazard: ");
    printBoolVector(equipmentInfo.getCanTranportHazard());
    std::cout << "Times Used: " << equipmentInfo.getTimesUsed() << std::endl;
    std::cout << "Times used limit: " << equipmentInfo.getTimesUsedLimit() << std::endl;
    print("Weight limit: ");
    std::cout << equipmentInfo.getWeightLimit() << std::endl;
    print("Weight left: ");
    std::cout << equipmentInfo.getWeightLeft() << std::endl;
}

void printFullInfoEmployee(Employee employeeInfo)
{
    print("Employee info: ");
    print("getAssignedEquipment: ");
    printFullInfoEquipment(employeeInfo.getAssignedEquipment());
    print("getCanRepair: ");
    std::cout << employeeInfo.getCanRepair() << std::endl;
    print("getEquipmentTraining: ");
    printBoolVector(employeeInfo.getEquipmentTraining());
    print("getHazardTraining: ");
    printBoolVector(employeeInfo.getHazardTraining());
    print("getStatesTraining: ");
    printBoolVector(employeeInfo.getStatesTraining());
}

void printGoodVector(std::vector <Good> goodVector)
{
    int vectorSize = goodVector.size();
    for(int i = 0; i < vectorSize; i++)
    {
        std::cout << "vector[" << i << "]: " << std::endl;
        printFullInfoGood(goodVector[i]);
    }
}

void printEquipmentVector(std::vector <Equipment> equipmentInfo)
{
    int vectorSize = equipmentInfo.size();
    for(int i = 0; i < vectorSize; i++)
    {
        std::cout << "vector[" << i << "]: " << std::endl;
        printFullInfoEquipment(equipmentInfo[i]);
    }
}

void printEmployeeVector(std::vector <Employee> employeeInfo)
{
    int vectorSize = employeeInfo.size();
    for(int i = 0; i < vectorSize; i++)
    {
        std::cout << "vector[" << i << "]: " << std::endl;
        printFullInfoEmployee(employeeInfo[i]);
    }
}





void testGoodGetHazard()
{
    print("testGoodGetHazard");
    Good gold;
    print("Object Hazards: ");
    printBoolVector(gold.getHazard());
}

void testGoodGetSize_()
{
    print("testGoodGetSize_");
    Good gold;
    print("Object size: ");
    printIntVector(gold.getSize_());
}

void testGoodGetStateOfMatter()
{
    print("testGoodGetStateOfMatter");
    Good gold;
    std::cout << "object state of matter is: " <<  gold.getStateOfMatter() << std::endl;
}

void testGoodGetWeight()
{
    print("testGoodGetWeight");
    Good gold;
    std::cout << "object weight is: " << gold.getWeight() << std::endl;
}

void testGoodGetters()
{
    print("testGoodGetters");
    testGoodGetHazard();
    testGoodGetSize_();
    testGoodGetStateOfMatter();
    testGoodGetWeight();
}

void testGoodSetHazard()
{
    print("testGoodSetHazard");
    Good gold;
    gold.setHazard({0, 1, 1, 0});
    if(gold.getHazard()[1] != 1 || gold.getHazard()[2] != 1)
    {
        error_message("good.setHazard does not work");
    }
    print("Object hazard is: ");
    printBoolVector(gold.getHazard());
}

void testGoodSetSize_()
{
    print("testGoodSetSize_");
    Good gold;
    gold.setSize_({2, 2, 2});
    if(gold.getSize_()[0] != 2 || gold.getSize_()[1] != 2
       || gold.getSize_()[2] != 2)
    {
        error_message("good.setSize_ does not work");
    }
    print("Object size is: ");
    printIntVector(gold.getSize_());
}

void testGoodSetStateOfMatter()
{
    print("testGoodSetStateOfMatter");
    Good gold;
    gold.setStateOfMatter(3);
    if(gold.getStateOfMatter() != 0)
    {
        error_message("good.setStateOfMatter does not work");
    }
    std::cout << "Object State of Matter is: " << gold.getStateOfMatter() << std::endl;
    gold.setStateOfMatter(10);
    if(gold.getStateOfMatter() != 0)
    {
        error_message("good.setStateOfMatter does not work");
    }
    std::cout << "Object State of Matter is: " << gold.getStateOfMatter() << std::endl;
    gold.setStateOfMatter(1);
    if(gold.getStateOfMatter() != 1)
    {
        error_message("good.setStateOfMatter does not work");
    }
    std::cout << "Object State of Matter is: " << gold.getStateOfMatter() << std::endl;
}

void testGoodSetWeight()
{
    print("testGoodSetWeight");
    Good gold;
    gold.setWeight(100);
    if(gold.getWeight() != 100)
    {
        error_message("good.setStateOfMatter does not work");
    }
    std::cout << "Object weight is: " << gold.getWeight() << std::endl;
}

void testGoodSetters()
{
    print("testGoodSetters");
    testGoodSetHazard();
    testGoodSetSize_();
    testGoodSetStateOfMatter();
    testGoodSetWeight();
}

void testVolume()
{
    print("testGoodVolume");
    Good gold;
    if(gold.volume() != 0)
    {
        error_message("error in good.volume() method");
    }
    std::cout << "Volume of the good is equal to: " << gold.volume() << std::endl;
    gold.setSize_({2, 2, 2});
    if(gold.volume() != 8)
    {
        error_message("error in good.volume() method");
    }
    std::cout << "Volume of the good is equal to: " << gold.volume() << std::endl;
}



void testEquipmentGetSizeLimit()
{
    print("testEquipmentGetSizeLimit");
    Equipment forklift;
    printIntVector(forklift.getSizeLimit());
}

void testEquipmentGetSizeOccupied()
{
    print("testEquipmentGetSizeOccupied");
    Equipment forklift;
    printIntVector(forklift.getSizeLeft());
}

void testEquipmentGetCanTransportState()
{
    print("testEquipmentGetCanTransportState");
    Equipment forklift;
    printBoolVector(forklift.getCanTransportState());
}

void testEquipmentGetCanTranportHazard()
{
    print("testEquipmentGetCanTranportHazard");
    Equipment forklift;
    printBoolVector(forklift.getCanTranportHazard());
}

void testEquipmentGetTimesUsed()
{
    print("testEquipmentGetTimesUsed");
    Equipment forklift;
    std::cout << "Times used value is equal to: " << forklift.getTimesUsed() << std::endl;
}

void testEquipmentGetTimesUsedLimit()
{
    print("testEquipmentGetTimesUsedLimit");
    Equipment forklift;
    std::cout << "Times Used Limit value is equal to: " << forklift.getTimesUsedLimit() << std::endl;
}

void testEquipmentGetters()
{
    print("Test equipment getters");
    testEquipmentGetSizeLimit();
    testEquipmentGetSizeOccupied();
    testEquipmentGetCanTransportState();
    testEquipmentGetCanTranportHazard();
    testEquipmentGetTimesUsed();
    testEquipmentGetTimesUsedLimit();
}

void testEquipmentSetSizeLimit()
{
    print("testEquipmentSetSizeLimit");
    Equipment forklift;
    forklift.setSizeLimit({2, 2, 2});
    if(forklift.getSizeLimit()[0] != 2)
    {
        error_message("error in equipment.setSizeLimit");
    }
    printIntVector(forklift.getSizeLimit());
    forklift.setSizeLimit({0, 0, 0});
    if(forklift.getSizeLimit()[0] != 0)
    {
        error_message("error in equipment.setSizeLimit");
    }
    printIntVector(forklift.getSizeLimit());
    forklift.setSizeLimit({-2, -2, -2});
    if(forklift.getSizeLimit()[0] != 0)
    {
        error_message("error in equipment.setSizeLimit");
    }
    printIntVector(forklift.getSizeLimit());
}

void testEquipmentSetSizeOccupied()
{
    print("testEquipmentSetSizeOccupied");
    Equipment forklift;
    forklift.setSizeLeft({2, 2, 2});
    if(forklift.getSizeLeft()[0] != 0)
    {
        error_message("error in equipment.setSizeLeft");
    }
    printIntVector(forklift.getSizeLeft());
    forklift.setSizeLimit({3, 3, 3});
    forklift.setSizeLeft({2, 2, 2});
    if(forklift.getSizeLeft()[0] != 2)
    {
        error_message("error in equipment.setSizeLeft");
    }
    printIntVector(forklift.getSizeLeft());
}

void testEquipmentSetCanTransportState()
{
    print("testEquipmentSetCanTransportState");
    Equipment forklift;
    forklift.setCanTransportState({1, 1, 1});
    if(forklift.getCanTransportState()[0] != 1)
    {
        error_message("error in equipment.setCanTransportState");
    }
    printBoolVector(forklift.getCanTransportState());
}

void testEquipmentSetCanTransportHazard()
{
    print("testEquipmentSetCanTransportHazard");
    Equipment forklift;
    forklift.setCanTransportHazard({1, 1, 1, 1});
    if(forklift.getCanTranportHazard()[0] != 1)
    {
        error_message("error in equipment.SetCanTransportHazard");
    }
    printBoolVector(forklift.getCanTranportHazard());
}

void testEquipmentSetTimesUsed()
{
    print("testEquipmentSetTimesUsed");
    Equipment forklift;
    forklift.setTimesUsed(5);
    if(forklift.getTimesUsed() != 5)
    {
        error_message("Error in equipment.setTimesUsed");
    }
    std::cout << "Times Used value is: " << forklift.getTimesUsed() << std::endl;
    forklift.setTimesUsed(-5);
    if(forklift.getTimesUsed() != 5)
    {
        error_message("Error in equipment.setTimesUsed");
    }
    std::cout << "Times Used value is: " << forklift.getTimesUsed() << std::endl;

}

void testEquipmentSetTimesUsedLimit()
{
    print("testEquipmentSetTimesUsedLimit");
    Equipment forklift;
    forklift.setTimesUsedLimit(5);
    if(forklift.getTimesUsedLimit() != 5)
    {
        error_message("Error in equipment.setTimesUsedLimit");
    }
    std::cout << "Times Used Limit value is: " << forklift.getTimesUsedLimit() << std::endl;
    forklift.setTimesUsedLimit(-5);
    if(forklift.getTimesUsedLimit() != 5)
    {
        error_message("Error in equipment.setTimesUsedLimit");
    }
    std::cout << "Times Used Limit value is: " << forklift.getTimesUsedLimit() << std::endl;
}

void testEquipmentSetters()
{
    print("Test equipment setters");
    testEquipmentSetSizeLimit();
    testEquipmentSetSizeOccupied();
    testEquipmentSetCanTransportState();
    testEquipmentSetCanTransportHazard();
    testEquipmentSetTimesUsed();
    testEquipmentSetTimesUsedLimit();
}

void testCanMoveGoodHazard()
{
    print("testCanMoveGoodHazard");
    Good gold;
    Equipment forklift;
    if(!forklift.canMoveHazard(gold))
    {
        error_message("error in equipment.canMoveHazard");
    }
    std::cout << forklift.canMoveHazard(gold) << std::endl;
    gold.setHazard({1, 0, 0});
        if(forklift.canMoveHazard(gold))
    {
        error_message("error in equipment.canMoveHazard");
    }
    std::cout << forklift.canMoveHazard(gold) << std::endl;
    forklift.setCanTransportHazard({1, 0, 0});
    if(!forklift.canMoveHazard(gold))
    {
        error_message("error in equipment.canMoveHazard");
    }
    std::cout << forklift.canMoveHazard(gold) << std::endl;
}

void testCanMoveGoodState()
{
    std::cout << "testCanMoveGoodState" << std::endl;
    Good gold;
    Equipment forklift;
    if(forklift.canMoveState(gold))
    {
        error_message("error in equipmentCanMoveState");
    }
    std::cout << forklift.canMoveState(gold) << std::endl;
    forklift.setCanTransportState({1, 0, 0});
    if(!forklift.canMoveState(gold))
    {
        error_message("error in equipmentCanMoveState");
    }
    std::cout << forklift.canMoveState(gold) << std::endl;
    forklift.setCanTransportState({0, 1, 0});
    if(forklift.canMoveState(gold))
    {
        error_message("error in equipment.CanMoveState");
    }
    std::cout << forklift.canMoveState(gold) << std::endl;
}

void testCanMoveGoodSize()
{
    std::cout << "testCanMoveGoodSize" << std::endl;
    Good gold;
    Equipment forklift;
    if(!forklift.canMoveSize(gold))
    {
        error_message("error in equipment.CanMoveSize");
    }
    std::cout << forklift.canMoveSize(gold) << std::endl;
    gold.setSize_({1, 1, 1});
    if(forklift.canMoveSize(gold))
    {
        error_message("error in equipment.CanMoveSize");
    }
    std::cout << forklift.canMoveSize(gold) << std::endl;
    forklift.setSizeLimit({2, 2, 2});
    if(!forklift.canMoveSize(gold))
    {
        error_message("error in equipment.CanMoveSize");
    }
    std::cout << forklift.canMoveSize(gold) << std::endl;
    gold.setSize_({1, 1, 3});
    if(forklift.canMoveSize(gold))
    {
        error_message("error in equipment.CanMoveSize");
    }
    std::cout << forklift.canMoveSize(gold) << std::endl;
    gold.setSize_({1, 3, 1});
    if(forklift.canMoveSize(gold))
    {
        error_message("error in equipment.CanMoveSize");
    }
    std::cout << forklift.canMoveSize(gold) << std::endl;
    gold.setSize_({3, 1, 1});
    if(forklift.canMoveSize(gold))
    {
        error_message("error in equipment.CanMoveSize");
    }
    std::cout << forklift.canMoveSize(gold) << std::endl;
}

void testCanMoveGoodAll()
{
    print("testCanMoveGoodAll()");
    Good gold;
    Equipment forklift;
    if(forklift.canMoveGood(gold))
    {
        error_message("equipment.canMoveGood");
    }
    std::cout << forklift.canMoveGood(gold) << std::endl;
    gold.setHazard({1, 0, 0, 0});
    gold.setSize_({1, 1, 2});
    gold.setStateOfMatter(1);
    if(forklift.canMoveGood(gold))
    {
        error_message("equipment.canMoveGood");
    }
    std::cout << forklift.canMoveGood(gold) << std::endl;
    forklift.setCanTransportHazard({0, 1, 1, 1});
    forklift.setSizeLimit({3, 3, 3});
    forklift.setCanTransportState({1, 1, 1});
    if(forklift.canMoveGood(gold))
    {
        error_message("equipment.canMoveGood");
    }
    std::cout << forklift.canMoveGood(gold) << std::endl;
    forklift.setCanTransportHazard({1, 1, 1, 1});
    forklift.setSizeLimit({3, 3, 1});
    forklift.setCanTransportState({1, 1, 1});
    if(forklift.canMoveGood(gold))
    {
        error_message("equipment.canMoveGood");
    }
    std::cout << forklift.canMoveGood(gold) << std::endl;
    forklift.setCanTransportHazard({1, 1, 1, 1});
    forklift.setSizeLimit({3, 3, 3});
    forklift.setCanTransportState({1, 0, 1});
    if(forklift.canMoveGood(gold))
    {
        error_message("equipment.canMoveGood");
    }
    std::cout << forklift.canMoveGood(gold) << std::endl;
    forklift.setCanTransportHazard({1, 1, 1, 1});
    forklift.setSizeLimit({3, 3, 3});
    forklift.setCanTransportState({1, 1, 1});
    if(forklift.canMoveGood(gold))
    {
        error_message("equipment.canMoveGood");
    }
    std::cout << forklift.canMoveGood(gold) << std::endl;
}

void testCanMoveGood()
{
    print("testCanMoveGood");
    testCanMoveGoodHazard();
    testCanMoveGoodState();
    testCanMoveGoodSize();
    testCanMoveGoodAll();
}

void testTimesUsed()
{
    print("testTimesUsed");
    Equipment forklift;
    forklift.setTimesUsedLimit(10);
    if(forklift.needsRepair())
    {
        error_message("equipment.needsRepair");
    }
    std::cout << forklift.needsRepair() << std::endl;
    forklift.setTimesUsed(20);
    if(!forklift.needsRepair())
    {
        error_message("equipment.needsRepair");
    }
    std::cout << forklift.needsRepair() << std::endl;
    forklift.setTimesUsedLimit(30);
    if(forklift.needsRepair())
    {
        error_message("equipment.needsRepair");
    }
    std::cout << forklift.needsRepair() << std::endl;
 }

void testEquipmentVolumeLimit()
{
    print("testEquipmentVolumeLimit");
    Equipment forklift;
    if(forklift.volumeLimit() != 0)
    {
        error_message("equipment.volumeLimit");
    }
    std::cout << "equipment volume equal to: " << forklift.volumeLimit() << std::endl;
    forklift.setSizeLimit({1, 1, 1});
    if(forklift.volumeLimit() != 1)
    {
        error_message("equipment.volumeLimit");
    }
    std::cout << "equipment volume equal to: " << forklift.volumeLimit() << std::endl;
    forklift.setSizeLimit({1, 1, 0});
    if(forklift.volumeLimit() != 0)
    {
        error_message("equipment.volumeLimit");
    }
    std::cout << "equipment volume equal to: " << forklift.volumeLimit() << std::endl;
}

void testEquipmentVolumeOccupied()
{
    print("testEquipmentVolumeOccupied");
    Equipment forklift;
    if(forklift.volumeLeft() != 0)
    {
        error_message("equipment.volumeLimit");
    }
    std::cout << "equipment volume equal to: " << forklift.volumeLeft() << std::endl;
    forklift.setSizeLeft({1, 1, 1});
    if(forklift.volumeLeft() != 0)
    {
        error_message("equipment.volumeLimit");
    }
    std::cout << "equipment volume equal to: " << forklift.volumeLeft() << std::endl;
    forklift.setSizeLimit({2, 2, 2});
    forklift.setSizeLeft({1, 1, 1});
    if(forklift.volumeLeft() != 1)
    {
        error_message("equipment.volumeLimit");
    }
    std::cout << "equipment volume equal to: " << forklift.volumeLeft() << std::endl;
}

void testEquipmentChangeSizeGood()
{
    print("testEquipmentChangeSizeGood");
    Equipment forklift;
    Good gold;
    forklift.occupySpaceGood(gold);
    if(forklift.getSizeLeft()[0] != 0)
    {
        error_message("Error in equipment.occupySpaceGood");
    }
    printIntVector(forklift.getSizeLeft());
    gold.setSize_({1, 1, 1});
    forklift.occupySpaceGood(gold);
    if(forklift.getSizeLeft()[0] != 0)
    {
        error_message("Error in equipment.occupySpaceGood");
    }
    printIntVector(forklift.getSizeLeft());
    forklift.setSizeLimit({2, 2, 2});
    forklift.occupySpaceGood(gold);
    if(forklift.getSizeLeft()[0] != 1)
    {
        error_message("Error in equipment.occupySpaceGood");
    }
    printIntVector(forklift.getSizeLeft());

}



void testEmployeeGetEquipmentTraining()
{
    print("testEmployeeGetEquipmentTraining");
    Employee marcel;
    printBoolVector(marcel.getEquipmentTraining());
}

void testEmployeeGetHazardTraining()
{
    print("testEmployeeGetHazardTraining");
    Employee marcel;
    printBoolVector(marcel.getHazardTraining());
}

void testEmployeeGetStatesTraining()
{
    print("testEmployeeGetStatesTraining");
    Employee marcel;
    printBoolVector(marcel.getStatesTraining());
}

void testEmployeeGetAssignedEquipment()
{
    print("testEmployeeGetAssignedEquipment");
    Employee marcel;
    printFullInfoEquipment(marcel.getAssignedEquipment());

}

void testEmployeeGetCanRepair()
{
    print("testEmployeeGetCanRepair");
    Employee marcel;
    std::cout << marcel.getCanRepair();
}

void testEmployeeGetters()
{
    print("Test employee Getters ");
    testEmployeeGetEquipmentTraining();
    testEmployeeGetHazardTraining();
    testEmployeeGetStatesTraining();
    testEmployeeGetAssignedEquipment();
    testEmployeeGetCanRepair();
}

void testEmployeeSetEquipmentTraining()
{
    print("testEmployeeSetEquipmentTraining");
    Employee marcel;
    if(marcel.getEquipmentTraining()[0] != 0)
    {
        error_message("employee.setEquipmentTraining");
    }
    printBoolVector(marcel.getEquipmentTraining());
    marcel.trainEquipment(2);
    if(marcel.getEquipmentTraining()[2] != 1)
    {
        error_message("employee.setEquipmentTraining");
    }
    printBoolVector(marcel.getEquipmentTraining());
    marcel.trainEquipment(-5);
    if(marcel.getEquipmentTraining()[5] != 0)
    {
        error_message("employee.setEquipmentTraining");
    }
    printBoolVector(marcel.getEquipmentTraining());
    marcel.trainEquipment(20);
    if(marcel.getEquipmentTraining()[0] != 0)
    {
        error_message("employee.setEquipmentTraining");
    }
    printBoolVector(marcel.getEquipmentTraining());
}

void testEmployeeSetHazardTraining()
{
    print("testEmployeeSetHazardTraining");
    Employee marcel;
    if(marcel.getHazardTraining()[0] != 0)
    {
        error_message("employee.setHazardTraining");
    }
    printBoolVector(marcel.getHazardTraining());
    marcel.trainHazard(1);
    if(marcel.getHazardTraining()[1] != 1)
    {
        error_message("employee.setHazardTraining");
    }
    printBoolVector(marcel.getHazardTraining());
    marcel.trainHazard(9);
    if(marcel.getHazardTraining()[0] != 0)
    {
        error_message("employee.setHazardTraining");
    }
    printBoolVector(marcel.getHazardTraining());
    marcel.trainHazard(-4);
    if(marcel.getHazardTraining()[0] != 0)
    {
        error_message("employee.setHazardTraining");
    }
    printBoolVector(marcel.getHazardTraining());
}

void testEmployeeSetStatesTraining()
{
    print("testEmployeeSetStatesTraining");
    Employee marcel;
    if(marcel.getStatesTraining()[0] != 0)
    {
        error_message("employee.setStatesTraining");
    }
    printBoolVector(marcel.getStatesTraining());
    marcel.trainStates(1);
    if(marcel.getStatesTraining()[1] != 1)
    {
        error_message("employee.setStatesTraining");
    }
    printBoolVector(marcel.getStatesTraining());
    marcel.trainStates(6);
    if(marcel.getStatesTraining()[1] != 1)
    {
        error_message("employee.setStatesTraining");
    }
    printBoolVector(marcel.getStatesTraining());
    marcel.trainStates(-3);
    if(marcel.getStatesTraining()[1] != 1)
    {
        error_message("employee.setStatesTraining");
    }
    printBoolVector(marcel.getStatesTraining());
}

void testEmployeeSetAssignedEquipment()
{
    print("testEmployeeSetAssignedEquipment");
    Employee marcel;
    Equipment forklift;
    forklift.setCanTransportHazard({1, 1, 1});
    forklift.setCanTransportState({1, 1, 1});
    forklift.setSizeLimit({2, 2, 2});
    forklift.setTimesUsed(1);
    forklift.setTimesUsedLimit(20);
    forklift.setTrainingRequired(1);
    marcel.assignEquipment(forklift);
    if(marcel.canAssignEquipment(forklift))
    {
        error_message("error in employee.canAssignEquipment");
    }
    printFullInfoEquipment(marcel.getAssignedEquipment());
    marcel.trainEquipment(1);
    marcel.assignEquipment(forklift);
    if(!marcel.canAssignEquipment(forklift))
    {
        error_message("error in employee.canAssignEquipment");
    }
    printFullInfoEquipment(marcel.getAssignedEquipment());
    marcel.removeEquipment();
    printFullInfoEquipment(marcel.getAssignedEquipment());
}

void testEmployeeSetCanRepair()
{
    print("testEmployeeSetCanRepair");
    Employee marcel;
    if(marcel.getCanRepair())
    {
        error_message("Error in employee.setRepair");
    }
    std::cout << marcel.getCanRepair() << std::endl;
    marcel.trainRepair();
    if(!marcel.getCanRepair())
    {
        error_message("Error in employee.setRepair");
    }
    std::cout << marcel.getCanRepair() << std::endl;
}


void testEmployeeSetters()
{
    print("Test employee Setters ");
    testEmployeeSetEquipmentTraining();
    testEmployeeSetHazardTraining();
    testEmployeeSetStatesTraining();
    testEmployeeSetAssignedEquipment();
    testEmployeeSetCanRepair();
}

void testEmployeeRepairEquipment()
{
    print("testEmployeeRepairEquipment");
    Employee marcel;
    Equipment forklift;
    forklift.setTimesUsedLimit(10);
    std::cout << marcel.repairEquipment(forklift) << std::endl;
    if(forklift.getTimesUsed() != 0)
    {
        error_message("employee.repairEquipment");
    }
    std::cout << "times used: " << forklift.getTimesUsed() << std::endl;
    forklift.setTimesUsed(20);
    std::cout << marcel.repairEquipment(forklift) << std::endl;
    if(forklift.getTimesUsed() != 20)
    {
        error_message("employee.repairEquipment");
    }
    std::cout << "times used: " << forklift.getTimesUsed() << std::endl;
    marcel.trainRepair();
    std::cout << marcel.repairEquipment(forklift) << std::endl;
    if(forklift.getTimesUsed() != 0)
    {
        error_message("employee.repairEquipment");
    }
    std::cout << "times used: " << forklift.getTimesUsed() << std::endl;
    std::cout << marcel.repairEquipment(forklift) << std::endl;
    if(forklift.getTimesUsed() != 0)
    {
        error_message("employee.repairEquipment");
    }
    std::cout << "times used: " << forklift.getTimesUsed() << std::endl;
}

void testEmployeeMoveGood()
{
    print("testEmployeeMoveGood");
    Employee marcel;
    Equipment forklift_1;
    Equipment forklift_2;
    Good gold;
    gold.setSize_({2, 2, 2});
    forklift_1.setSizeLimit({3, 3, 3});
    forklift_2.setSizeLimit({4, 4, 4});
    if(marcel.canMoveGood(gold, forklift_1, forklift_2))
    {
        error_message("employee.canMoveGood");
    }
    std::cout << marcel.moveGood(gold, forklift_1, forklift_2) << std::endl;
    forklift_1.setCanTransportState({1, 1, 1});
    forklift_2.setCanTransportState({1, 1, 1});
    forklift_1.setTimesUsedLimit({1});
    forklift_2.setTimesUsedLimit({1});
    if(marcel.canMoveGood(gold, forklift_1, forklift_2))
    {
        error_message("employee.canMoveGood");
    }
    std::cout << marcel.moveGood(gold, forklift_1, forklift_2) << std::endl;
    marcel.trainStates(0);
    if(!marcel.canMoveGood(gold, forklift_1, forklift_2))
    {
        error_message("employee.canMoveGood");
    }
    std::cout << marcel.moveGood(gold, forklift_1, forklift_2) << std::endl;
    printIntVector(forklift_2.getSizeLeft());
}

void testGoods()
{
    print("testGoods");
    testGoodGetters();
    testGoodSetters();
    testVolume();
}

void testEquipment()
{
    print("testEquipment");
    testEquipmentGetters();
    testEquipmentSetters();
    testCanMoveGood();
    testTimesUsed();
    testEquipmentVolumeLimit();
    testEquipmentVolumeOccupied();
    testEquipmentChangeSizeGood();
}

void testEmployee()
{
    print("testEmployee");
    testEmployeeGetters();
    testEmployeeSetters();
    testEmployeeRepairEquipment();
    testEmployeeMoveGood();
}

void testWarehouseGetters()
{
    print("testWarehouseGetters");
    Warehouse magazyn;
    printGoodVector(magazyn.getAllGoods());
    printEquipmentVector(magazyn.getAllEquipment());
    printEmployeeVector(magazyn.getAllEmployees());
}

void testWarehouseAddEquipment()
{
    print("testWarehouseAddEquipment");
    Warehouse magazyn;
    Equipment forklift;
    magazyn.addEquipment(forklift);
    printEquipmentVector(magazyn.getAllEquipment());
}

void testWarehouseAddEmployee()
{
    Warehouse magazyn;
    Employee marcel;
    magazyn.addEmployee(marcel);
    printEmployeeVector(magazyn.getAllEmployees());
    marcel.trainEquipment(5);
    printEmployeeVector(magazyn.getAllEmployees());
}

void testWarehouseAddGood()
{
    print("testWarehouseAddGood");
    Warehouse magazyn;
    Good gold;
    magazyn.addGood(gold);
    printGoodVector(magazyn.getAllGoods());
    Employee marcel;
    magazyn.addEmployee(marcel);
    magazyn.addGood(gold);
    printGoodVector(magazyn.getAllGoods());
    marcel.trainStates(0);
    magazyn.addGood(gold);
    printGoodVector(magazyn.getAllGoods());
    Equipment forklift;
    magazyn.addEquipment(forklift);
    magazyn.addGood(gold);
    printGoodVector(magazyn.getAllGoods());
    forklift.setCanTransportState({1, 1, 1});
    magazyn.addGood(gold);
    printGoodVector(magazyn.getAllGoods());
    forklift.setTimesUsedLimit(20);
    magazyn.addGood(gold);
    printGoodVector(magazyn.getAllGoods());
}

void testWarehouseAdd()
{
    print("testWarehouseAdd");
    testWarehouseAddEquipment();
    testWarehouseAddEmployee();
    testWarehouseAddGood();
}

void testWarehouse()
{
    print("testWarehouse");
    testWarehouseGetters();
    testWarehouseAdd();
}

int main()
{
    testGoods();
    testEquipment();
    testEmployee();
    testWarehouse();
    return 0;
}
