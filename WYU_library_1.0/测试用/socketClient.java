/*********************************
 客户端，测试用
 ********************************/



import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.*;

public class socketClient {  
    public static void main(String[] args) {  
        try {
               Socket s = new Socket("192.168.0.240",6666);
               
               //构建IO
               InputStream is = s.getInputStream();
               OutputStream os = s.getOutputStream();
               
               BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(os));
               //向服务器端发送一条消息
               String data[] = new String[100]; 
               data[0] = "3118001162";
               data[1] = "cwh13671461740";
               //Scanner in = new Scanner(System.in);
               //data[2] = in.nextLine();
               for(int i = 0; i < 2; i++){
                  bw.write(data[i]);
               }
               System.out.println("数据发送成功...");
               bw.flush();
               
               byte[] bytes = new byte[102400];
               int len;
               String rcv_end = new String("-1");
               StringBuilder sb = new StringBuilder();
               while ((len = is.read(bytes)) != -1) {
                  String str = new String(bytes, 0, len,"UTF-8");
                  if(str.equals(rcv_end)){//数据接收结束位
                     break;
                  }

                  sb.append(str);
               }
               System.out.println( sb);
         } 
         catch (UnknownHostException e) {
            e.printStackTrace();
         } 
         catch (IOException e) {
            e.printStackTrace();
         }
    }  
}  