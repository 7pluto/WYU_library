package com.example.wyu_library;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;
//https://blog.csdn.net/bzlj2912009596/article/details/79648520

public class TextViewActivity extends AppCompatActivity {
    private LinearLayout mContainer;
    private Button mBt1;
    private String[] str;
    static StringBuilder dataPrint;//接收的数据
    ArrayList<String> startDay = new ArrayList<String>();
    ArrayList<String> endDay = new ArrayList<String>();
    ArrayList<String> book = new ArrayList<String>();
    private String data = new String("123");

    public void Setdata(StringBuilder sa){//接收数据
        dataPrint = sa;
        //Log.d("aas","data:"+dataPrint);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_text_view);

        mContainer = findViewById(R.id.container);
        str = dataPrint.toString().split("\n");
        int len = str.length;

        //分割字符，提取信息
        int k = 0;
        while(k < len - 1)
        {
            startDay.add(str[k++]);//0 4 开始日期
            endDay.add(str[k++]);//1 5   结束日期
            book.add(str[k++]); // 2 6   书籍名称
            k++;//3 7书籍登录号，暂时丢弃
        }

        //显示界面需要制作优化
        for(int i = 0; i < startDay.size() ; i++)
        {
            //添加文本,this代表当前项目
            TextView tv = new TextView(this);
            tv.setText(startDay.get(i) + " "+endDay.get(i)+ " " + book.get(i));
            //tv.setText("" + i);
            tv.setId(i);
            mContainer.addView(tv);
        }
        mBt1 = findViewById(R.id.bt_1);
        mBt1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //与esp8266连接，发送数据
                Esp8266Socket espS = new Esp8266Socket();
                espS.start();
                //发送的数据被定死，需要在UI中提供选择
                Toast.makeText(TextViewActivity.this,"发送成功！",Toast.LENGTH_SHORT).show();
            }
        });
    }

    public class Esp8266Socket extends Thread {
        public void run() {
            try {
                Socket s = new Socket("192.168.0.40",8266);

                OutputStream os = s.getOutputStream();
                BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(os));

                int tmp = 0;
                bw.write(book.get(tmp));
                bw.write(endDay.get(tmp));
                System.out.println("数据发送成功...");
                bw.flush();
            }
            catch (UnknownHostException e) {
                e.printStackTrace();
            }
            catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
