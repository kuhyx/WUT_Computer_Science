#ifndef GOOD_HPP
#define GOOD_HPP
#include <vector>

class Good
{
    private:
        std::vector<int> size_;
        std::vector<bool> hazard;
        int stateOfMatter;
        unsigned int weight;

    public:

        Good();

        std::vector <int> getSize_() const;
        std::vector <bool> getHazard() const;
        int getStateOfMatter() const;
        int getWeight() const;

        void setSize_(std::vector <int> newSize);
        void setHazard(std::vector <bool> newHazard);
        void setStateOfMatter(int newState);
        void setWeight(int newWeight);


        int volume();



};

#endif // GOOD
