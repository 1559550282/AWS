package com.example.demo.controller;

import com.example.demo.entity.Student;
import com.example.demo.repository.StudentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

/**
 * 描述
 *
 * @author wenwei_yang
 * @ClassName HomePageHandler
 * @Package com.example.demo.controller
 * @date 2021/7/13 12:09
 */
@Controller
public class HomePageHandler {

    @Autowired
    private StudentRepository studentRepository;

    @GetMapping("")
    public String index(Model model) {
        model.addAttribute("fields", Student.class.getDeclaredFields());
        model.addAttribute("students", studentRepository.findAll());
        return "index";
    }

}
