#ifndef EQUIPMENT_HPP
#define EQUIPMENT_HPP

#include <vector>
#include "good.hpp"

class Equipment
{
    private:
        std::vector <bool> canTransportHazard;
        std::vector <bool> canTransportState;
        std::vector <int> sizeLimit;
        std::vector <int> sizeLeft;
        std::vector <bool> trainingRequired;
        int timesUsed;
        int timesUsedLimit;
        int weightLimit;
        int weightLeft;

    public:
        Equipment();


        bool canMoveHazard(Good &someGood);
        bool canMoveState(Good &someGood);
        bool canMoveSize(Good &someGood);
        bool canMoveGood(Good &someGood);
        void occupySpaceGood(Good &someGood);

        bool needsRepair() const;

        int volumeLimit() const;
        int volumeLeft() const;

        void setCanTransportState(std::vector<bool> newState);
        void setCanTransportHazard(std::vector <bool> newHazard);
        void setSizeLimit(std::vector <int> newSize);
        void setSizeLeft (std::vector <int> newSizeLeft);
        void setTimesUsed(int newTimesUsed);
        void setTimesUsedLimit(int newTimesUsedLimit);
        void setTrainingRequired(int trainingNumber);
        void setWeightLimit(int newWeightLimit);
        void setWeightLeft(int newWeightLeft);

        std::vector <int> getSizeLimit() const;
        std::vector <int> getSizeLeft() const;
        std::vector <bool> getCanTransportState() const;
        std::vector<bool> getCanTranportHazard() const;
        int getTimesUsed() const;
        int getTimesUsedLimit() const;
        int getWeightLimit() const;
        int getWeightLeft() const;
        std::vector<bool> getTrainingRequired() const;

        void operator = (Equipment const &otherEquipment);
};

#endif // EQUIPMENT
