#ifndef EMPLOYEE_HPP
#define EMPLOYEE_HPP

#include <vector>
#include "equipment.hpp"

class Employee
{
    private:
        std::vector <bool> equipmentTraining;
        std::vector <bool> hazardTraining;
        std::vector <bool> statesTraining;
        bool canRepair;
        Equipment assignedEquipment;

    public:
        Employee();

        std::vector <bool> getEquipmentTraining() const;
        std::vector <bool> getHazardTraining() const;
        std::vector <bool> getStatesTraining() const;
        Equipment getAssignedEquipment() const;
        bool getCanRepair() const;

        void trainEquipment(int certificateNumber);
        void trainHazard(int certificateNumber);
        void trainStates(int certificateNumber);
        void trainRepair();
        void assignEquipment(Equipment &newEquipment);
        void removeEquipment();

        bool canAssignEquipment(Equipment toBeAssigned) const;
        bool canEmployeeMoveGoodState(Good &goodToMove) const;
        bool canEmployeeMoveGoodHazard(Good &goodToMove) const;
        bool canEmployeeMoveGood(Good &goodToMove) const;
        bool canMoveGood(Good &goodToMove, Equipment &toWhichMove, Equipment &fromWhichMove) const;
        bool moveGood(Good &goodToMove, Equipment &toWhichMove, Equipment &fromWhichMove) const;
        void moveGoodOverride(Good &goodToMove, Equipment &toWhichMove) const;
        bool repairEquipment(Equipment &toRepair) const;


};



#endif
