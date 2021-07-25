package com.example.demo.repository.impl;

import com.example.demo.entity.Student;
import com.example.demo.repository.StudentRepository;
import org.springframework.stereotype.Repository;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Repository
public class StudentRepositoryImpl implements StudentRepository {
    private static Map<Long, Student> studentMap;

    static {
        studentMap = new HashMap<>();
        studentMap.put(1L, new Student(1L, "张三", 22, 66d));
        studentMap.put(2L, new Student(2L, "李四", 23, 68d));
        studentMap.put(3L, new Student(3L, "王五", 24, 65d));
    }

    @Override
    public List<Student> findAll() {
        return new ArrayList<>(studentMap.values());
    }

    @Override
    public Student findById(long id) {
        return studentMap.get(id);
    }

    @Override
    public void add(Student student) {
        studentMap.put(student.getId(), student);
    }

    @Override
    public void update(Student student) {
        Student old = studentMap.get(student.getId());
        Field[] fields = Student.class.getDeclaredFields();
        for (Field field : fields) {
            try {
                field.setAccessible(true);
                if (field.get(student) == null || field.get(student).equals("")) {
                    field.set(student, field.get(old));
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        studentMap.put(student.getId(), student);
    }

    @Override
    public void deleteById(long id) {
        studentMap.remove(id);
    }
}
