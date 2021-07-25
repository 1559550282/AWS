package com.example.demo.controller;

import com.example.demo.entity.Student;
import com.example.demo.repository.StudentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("student")
public class StudentHandler {
    @Autowired
    private StudentRepository studentRepository;

    @GetMapping("/list")
    public List<Student> findAll() {
        return studentRepository.findAll();
    }

    @GetMapping("{id}")
    public Student findById(@PathVariable("id") long id) {
        return studentRepository.findById(id);
    }

    @PostMapping("add")
    public void add(Student student, HttpServletResponse response) {
        List<Student> students = studentRepository.findAll();
        student.setId((long) (students.size() + 1));
        studentRepository.add(student);
        try {
            response.sendRedirect("/");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @PutMapping("update")
    public void update(Student student, HttpServletResponse response) {
        studentRepository.update(student);
        try {
            response.sendRedirect("/");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @DeleteMapping("{id}")
    public void deleteById(@PathVariable("id") long id, HttpServletResponse response) {
        studentRepository.deleteById(id);
        try {
            response.sendRedirect("/");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
