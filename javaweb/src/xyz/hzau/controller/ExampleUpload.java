package xyz.hzau.controller;

import java.io.*;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

public class ExampleUpload extends HttpServlet {

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {


        //System.out.println("1");

        response.setCharacterEncoding("UTF-8");
        response.setContentType("application/json; charset=utf-8");
        PrintWriter pw = response.getWriter();


        String fileName = request.getParameter("picture_name");
        String b = request.getParameter("type");

        //System.out.println(fileName+" "+b);
        //System.out.println("2");
        String uploadPath = request.getServletContext().getRealPath("") + File.separator + "upload";
        String filePath = uploadPath + File.separator+fileName;
        String command="";

        String return_data="";

        if (b.equals("number")){
            command="/bin/bash /root/tomcat_python/number.sh"+" "+filePath+" "+fileName;
            //System.out.println("3");
        }

        if (b.equals("plant")){
            command="/bin/bash /root/tomcat_python/plant.sh"+" "+filePath+" "+fileName;
            //System.out.println("3");
        }
        if (b.equals("insect")){
            command="/bin/bash /root/tomcat_python/insect.sh"+" "+filePath+" "+fileName;
            //System.out.println("3");
        }
        if (b.equals("yolo3")){
            command="/bin/bash /root/tomcat_python/yolo3.sh"+" "+filePath+" "+fileName;
            //System.out.println("3");
        }

        Process proc;
        try {

            //System.out.println("4");
            //proc = Runtime.getRuntime().exec("cmd /c activate & python D:\\PycharmProjects\\tensorflow1.13_py3.7\\finally\\linear_regression.py");
            proc = Runtime.getRuntime().exec(command);
            // 执行py文件
            //用输入输出流来截取结果
            BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
            String line = null;
            while ((line = in.readLine()) != null) {
                //System.out.println(line);
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
        System.out.println(return_data);

    }










    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {


        //String name = request.getParameter("which");


        //System.out.println("hello");
        response.setContentType("text/html;charset=utf-8");
        PrintWriter pw = response.getWriter();
        pw.println("hello,there is no doget,please use dopost");
    }
}