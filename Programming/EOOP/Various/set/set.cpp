#include "set.hpp"

Set::Set()
{
    data_ = {};
}

Set::~Set()
{
    data_.erase(data_.begin(), data_.end());
}

Set::Set(const Set& s)
{
    data_ = s.data_;
}

Set& Set::operator=(const Set& s)
{
    data_ = s.data_;
    return *this;
}

bool Set::isEmpty() const
{
    return data_.size() == 0;
}

SetData::size_type Set::size() const
{
    return data_.size();
}

void Set::add(int value)
{
    if(!contains(value)) data_.push_back(value);
}

Set Set::operator+(const Set& s) const
{
    Set newSet(s);
    for (unsigned int i = 0; i < data_.size(); ++i)
    {
        if(!newSet.contains(data_[i])) newSet.add(data_[i]);
    }
    return newSet;
}

Set& Set::operator+=(const Set& s)
{
    for(unsigned int i = 0; i < s.size(); ++i)
    {
        if(!contains(s.data_[i])) add(s.data_[i]);
    }
    return *this;
}

bool Set::contains(int value) const
{
    for(unsigned int i = 0; i < size(); ++i)
    {
        if(data_[i] == value) return 1;
    }
    return 0;
}

Set Set::operator-(const Set& s) const
{
    Set newSet;
    for(unsigned int i = 0; i < size(); ++i)
    {
        if(!s.contains(data_[i])) newSet.add(data_[i]);
    }
    return newSet;
}

void Set::remove(int value)
{
    if(contains(value))
    {
        for(unsigned int i = 0; i < size(); ++i)
        {
            if(data_[i] == value) data_.erase(data_.begin() + i);
        }
    }
}

Set& Set::operator-=(const Set& s)
{
    for(int i = size(); i >= 0; i--)
    {
        if(s.contains(data_[i])) remove(data_[i]);
    }
    return *this;
}

const int& Set::operator[](int index) const
{
    return data_[index];
}
