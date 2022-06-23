

#include "ring_buffer.hpp"
#include <array>
#include <iostream>
#include <stdexcept>

void error_message(const std::string& message, int value, int expected) {
    std::cerr << "Error - " << message << ", got: " << value << " expected " << expected << std::endl;
}

void error_message(const std::string& message) {
    std::cerr << "Error - " << message << "!" << std::endl;
}

void check_buffer(const RingBuffer& buffer, unsigned int expected_size, unsigned int expected_capacity) {
    bool is_empty = buffer.isEmpty();
    bool is_full = buffer.isFull();
    if (expected_size == 0) {
        if (!is_empty) {
            error_message("buffer should be empty");
        }
        if (is_full) {
            error_message("buffer shouldn't be full");
        }
    } else {
        if (is_empty) {
            error_message("buffer shouldn't be empty");
        }
        if ((expected_size == expected_capacity) && !is_full) {
            error_message("buffer should be full");
        }
    }
    unsigned int size = buffer.size();
    if (size != expected_size) {
        error_message("wrong buffer size", static_cast<int>(size), static_cast<int>(expected_size));
    }
    unsigned int capacity = buffer.capacity();
    if (capacity != expected_capacity) {
        error_message("wrong buffer capacity", static_cast<int>(capacity), static_cast<int>(expected_capacity));
    }
}

void check_empty_buffer() {
    unsigned int capacity = 4;
    RingBuffer buffer(capacity);
    check_buffer(buffer, 0, capacity);
}

void check_write_without_overwriting() {
    unsigned int capacity = 6;
    RingBuffer buffer(capacity);
    buffer.write(7);
    check_buffer(buffer, 1, capacity);

    buffer.write(42);
    check_buffer(buffer, 2, capacity);
}

void check_read_without_overwriting() {
    RingBuffer buffer(3);

    buffer.write(7);
    buffer.write(42);

    int read_number = buffer.read();
    if (read_number != 7) {
        error_message("read", read_number, 7);
    }
    read_number = buffer.read();
    if (read_number != 42) {
        error_message("read", read_number, 42);
    }
    check_buffer(buffer, 0, 3);
}

void _check_reading_after_overwrite(RingBuffer& buffer, unsigned int capacity) {
    for ( unsigned int i = 2; i <= capacity + 1; ++i ) {
        int read_number = buffer.read();
        if (read_number != static_cast<int>(i)) {
            error_message("read with overwrite", read_number, static_cast<int>(i));
        }
    }

    check_buffer(buffer, 0, capacity);
}

void check_overwriting() {
    unsigned int capacity = 4;
    RingBuffer buffer(capacity);

    for (unsigned int i = 0; i <= capacity + 1; ++i) {
        buffer.write(static_cast<int>(i));
    }
    check_buffer(buffer, capacity, capacity);

    _check_reading_after_overwrite(buffer, capacity);
}

void check_copy_constructor() {
    unsigned int capacity = 5;
    RingBuffer buffer(capacity);

    for (unsigned int i = 0; i <= capacity + 1; ++i) {
        buffer.write(static_cast<int>(i));
    }
    check_buffer(buffer, capacity, capacity);

    RingBuffer copied(buffer);

    check_buffer(copied, capacity, capacity);

    _check_reading_after_overwrite(buffer, capacity);
    _check_reading_after_overwrite(copied, capacity);
}

void check_assignment_operator() {
    unsigned int capacity = 5;
    RingBuffer buffer(capacity);
    RingBuffer other(capacity);

    for (unsigned int i = 0; i <= capacity + 1; ++i) {
        buffer.write(static_cast<int>(i));
    }
    check_buffer(buffer, capacity, capacity);
    check_buffer(other, 0, capacity);

    other = buffer;
    check_buffer(other, capacity, capacity);

    _check_reading_after_overwrite(buffer, capacity);
    _check_reading_after_overwrite(other, capacity);
}

void check_exceptions() {
    unsigned int capacity = 5;
    RingBuffer buffer(capacity);
    RingBuffer other(capacity - 1);

    try {
        buffer.read();
        error_message("missing exception while reading from empty buffer");
    } catch(std::exception& e) { }

    try {
        buffer = other;
        error_message("missing exception in copy constructor");
    } catch(std::exception& e) { }
}

int main() {
    check_empty_buffer();
    check_write_without_overwriting();
    check_read_without_overwriting();
    check_overwriting();
    check_copy_constructor();
    check_assignment_operator();
    check_exceptions();
    std::cout << "End of tests." << std::endl;
    return 0;
}
