package xyz.hzau.controller;

import org.apache.commons.fileupload.FileItem;
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.servlet.ServletFileUpload;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.Part;
import java.io.*;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;



/**
 * Servlet implementation class UploadServlet
 */

public class UploadPlant extends HttpServlet {
    private static final long serialVersionUID = 1L;

    // 上传文件存储目录
    private static final String UPLOAD_DIRECTORY = "upload";

    // 上传配置
    private static final int MEMORY_THRESHOLD   = 1024 * 1024 * 3;  // 3MB
    private static final int MAX_FILE_SIZE      = 1024 * 1024 * 40; // 40MB
    private static final int MAX_REQUEST_SIZE   = 1024 * 1024 * 50; // 50MB

    SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd_HH-mm-ss_");//设置日期格式

    /**
     * 上传数据及保存文件
     */
    protected void doPost(HttpServletRequest request,
                          HttpServletResponse response) throws ServletException, IOException {
        //System.out.println("hello");

        response.setCharacterEncoding("UTF-8");
        response.setContentType("application/json; charset=utf-8");

        PrintWriter writer = response.getWriter();

        // 检测是否为多媒体上传
        if (!ServletFileUpload.isMultipartContent(request)) {
            // 如果不是则停止
            writer.println("Error: 表单必须包含 enctype=multipart/form-data");
            writer.flush();
            return;
        }

        // 配置上传参数
        DiskFileItemFactory factory = new DiskFileItemFactory();
        // 设置内存临界值 - 超过后将产生临时文件并存储于临时目录中
        factory.setSizeThreshold(MEMORY_THRESHOLD);
        // 设置临时存储目录
        factory.setRepository(new File(System.getProperty("java.io.tmpdir")));

        ServletFileUpload upload = new ServletFileUpload(factory);

        // 设置最大文件上传值
        upload.setFileSizeMax(MAX_FILE_SIZE);

        // 设置最大请求值 (包含文件和表单数据)
        upload.setSizeMax(MAX_REQUEST_SIZE);

        // 中文处理
        upload.setHeaderEncoding("UTF-8");


        // 构造临时路径来存储上传的文件
        // 这个路径相对当前应用的目录
        String uploadPath = request.getServletContext().getRealPath("") + File.separator + UPLOAD_DIRECTORY;
        //String uploadPath = request.getServletContext().getRealPath("") + File.separator + UPLOAD_DIRECTORY;

//        System.out.println("1111:"+request.getServletContext().getRealPath(""));
//        System.out.println("uploadPath:"+uploadPath);
//        System.out.println("File.separator:"+File.separator);
//        System.out.println("UPLOAD_DIRECTORY:"+UPLOAD_DIRECTORY);

        // 如果目录不存在则创建
        File uploadDir = new File(uploadPath);
        if (!uploadDir.exists()) {
            uploadDir.mkdir();
        }

        try {
            // 解析请求的内容提取文件数据
            @SuppressWarnings("unchecked")
            List<FileItem> formItems = upload.parseRequest(request);

            if (formItems != null && formItems.size() > 0) {
                // 迭代表单数据
                for (FileItem item : formItems) {
                    // 处理不在表单中的字段
                    if (!item.isFormField()) {
                        String fileName = new File(item.getName()).getName();
                        String ip = request.getRemoteAddr();
                        fileName = df.format(new Date())+ip+'_'+fileName;
                        String filePath = uploadPath + File.separator+fileName;
                        File storeFile = new File(filePath);
                        // 在控制台输出文件的上传路径fileName
                        System.out.println(filePath);
                        System.out.println("fileName:"+fileName);
//                        System.out.println(uploadPath);
//                        System.out.println(fileName);
                        // 保存文件到硬盘
                        item.write(storeFile);
                        request.setAttribute("message",
                                "文件上传成功!");

                        ///***************************************************//

                        Process proc;
                        String return_data="";
                        try {

                            String command="/bin/bash /root/tomcat_python/plant.sh"+" "+filePath+" "+fileName;
                            //String command="cmd /c python D:\\demo1.py"+" "+filePath+" "+fileName;
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

                        System.out.println(return_data);
                        writer.println(return_data);


                        //////////*********************************************//


                    }
                }
            }
        } catch (Exception ex) {
            request.setAttribute("message",
                    "错误信息: " + ex.getMessage());
        }
        // 跳转到 message.jsp
//        request.getServletContext().getRequestDispatcher("/message.jsp").forward(
//                request, response);
    }
}
