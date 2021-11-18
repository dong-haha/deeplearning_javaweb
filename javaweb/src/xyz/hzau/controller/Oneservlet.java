package xyz.hzau.controller;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;

public class Oneservlet extends HttpServlet {

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {



        response.setContentType("text/html;charset=utf-8");
        PrintWriter pw = response.getWriter();


        String x = request.getParameter("str_x");
        String y = request.getParameter("str_y");
        String a = request.getParameter("a1_val");
        String b = request.getParameter("a2_val");
//        System.out.println(x);
//        System.out.println(a);

        String return_data="";

        Process proc;
        try {


            String command="/bin/bash /root/tomcat_python/linear_regression.sh"+" "+a+" "+b+" "+x+" "+y;
            //proc = Runtime.getRuntime().exec("cmd /c activate & python D:\\PycharmProjects\\tensorflow1.13_py3.7\\finally\\linear_regression.py");
            proc = Runtime.getRuntime().exec(command);
            // 执行py文件
            //用输入输出流来截取结果
            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            String line = null;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
                return_data= return_data+line;
            }
            in.close();
            proc.waitFor();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        pw.println(return_data);

    }










    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {


        //String name = request.getParameter("which");


        response.setContentType("text/html;charset=utf-8");
        PrintWriter pw = response.getWriter();
        pw.println("hello,there is no doget,please use dopost");
    }
}