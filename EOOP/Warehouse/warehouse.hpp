#ifndef WAREHOUSE_HPP
#define WAREHOUSE_HPP

#include <vector>
#include "employee.hpp"
#include "equipment.hpp"
#include "good.hpp"

class Warehouse
{
    private:

        std::vector <Employee*> allEmployees;
        std::vector <Equipment*> allEquipment;
        std::vector <Good*> allGoods;
        std::vector <int> size_;
    public:
        Warehouse();

        std::vector <Employee> getAllEmployees() const;
        std::vector<Equipment> getAllEquipment() const;
        std::vector<Good> getAllGoods() const;

        std::vector <int> findSuitableEmployees(Good &goodToShip);
        std::vector <int> findSuitableEquipments(Good &goodToShip);
        std::vector <int> equipmentAndEmployees(std::vector<int> goodEmployeesID, std::vector<int> goodEquipmentID);
        bool canShipGoods(std::vector <Good> &goodToShip);
        bool shipGoods(std::vector <Good> &goodsToShip);
        int calculateVolume() const;
        std::vector <int> capacityLeft() const;
        std::vector <int> capacityTotal() const;

        void addEmployee(Employee &newEmployee);
        void addEquipment(Equipment &equipmentToAdd);
        std::vector<int> canAddGood(Good &goodToAdd);
        bool addGood(Good &goodToShip);
        void addGoodOverride(Good &goodToShip);

};

#endif // WAREHOUSE
