package com.example.demo.repository;

import com.example.demo.entity.Student;

import java.util.List;

public interface StudentRepository {
    List<Student> findAll();

    Student findById(long id);

    void add(Student student);

    void update(Student student);

    void deleteById(long id);
}