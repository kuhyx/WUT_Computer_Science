#ifndef RINGBUFFER_HPP
#define RINGBUFFER_HPP
#include <stdlib.h>
#include <iostream>

class RingBuffer {
    public:
        explicit RingBuffer(unsigned int capacity): capacity_ (capacity)
        {
            head_ = 0;
            tail_ = 0;
            size_ = 0;
            overwritten = 0;
            data_ = (int *)malloc(capacity_);
        }
        RingBuffer(const RingBuffer& other);

        RingBuffer& operator=(const RingBuffer& other)
        {
            if(capacity_ != other.capacity_) throw std::exception();
            head_ = other.head_;
            tail_ = other.tail_;
            size_ = other.size_;
            overwritten = other.overwritten;
            data_ = (int *)malloc(capacity_);
            for(unsigned int i = 0; i < other.size_; i++)
            {
            data_[head_] = other.data_[head_];
            if(overwritten)
            {
            tail_ = (tail_ + 1) % capacity_;
            size_ = capacity_ - 1;
            }
            head_ = (head_ + 1) % capacity_;
            overwritten = (head_ == tail_);
            size_++;
            }
        }
        ~RingBuffer();

        unsigned int size() const { return size_; }
        unsigned int capacity() const { return capacity_; }
        bool isEmpty() const { return size_ == 0; }
        bool isFull() const { return size_ == capacity_; }

        int& read();

        void write(int value);

    private:
        const unsigned int capacity_;
        unsigned int size_;
        unsigned int head_;
        unsigned int tail_;
        int* data_;
        bool overwritten;
};

RingBuffer::~RingBuffer()
{
    if(data_)
    {
        delete data_;
        data_ = nullptr;
    }
}

void RingBuffer::write(int value)
{
    data_[head_] = value;
    if(overwritten)
    {
        tail_ = (tail_ + 1) % capacity_;
        size_ = capacity_ - 1;
    }
    head_ = (head_ + 1) % capacity_;
    overwritten = (head_ == tail_);
    size_++;
}

int& RingBuffer::read()
{
    if(size_ == 0) throw std::exception();

    int& answer = data_[tail_];
    overwritten = false;
    tail_ = (tail_ + 1) % capacity_;
    size_--;
    return answer;
}

RingBuffer::RingBuffer(const RingBuffer& other): capacity_ (other.capacity_)
{
    head_ = other.head_;
    tail_ = other.tail_;
    size_ = other.size_;
    overwritten = other.overwritten;
    data_ = (int *)malloc(capacity_);
    for(unsigned int i = 0; i < other.size_; i++)
    {
        data_[head_] = other.data_[head_];
        if(overwritten)
        {
            tail_ = (tail_ + 1) % capacity_;
            size_ = capacity_ - 1;
        }
        head_ = (head_ + 1) % capacity_;
        overwritten = (head_ == tail_);
        size_++;
    }
}

#endif  // RINGBUFFER_HPP
