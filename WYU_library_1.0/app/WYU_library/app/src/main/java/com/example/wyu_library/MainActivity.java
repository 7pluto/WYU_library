package com.example.wyu_library;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.Toast;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.net.UnknownHostException;


public class MainActivity extends AppCompatActivity {

    private Button mBtnLogin;
    private EditText mEtUserName;
    private EditText mEtPassword;
    private CheckBox mCBPsd;
    private SharedPreferences sharedPreferences;//记录输入框的
    private String SP_UserName = "sp_username";
    private String SP_PassWord = "sp_password";
    private String SP_REMEMBER_PSD = "sp_remember_psd";//记录多选框（是否记录账号）是否勾选
    private boolean mIsChecked = false;
    private String data[] = new String[100];//储存账号，用于发送
    private String[] recData = {};
    StringBuilder sb = new StringBuilder();//接收数据
    TextViewActivity tva = new TextViewActivity();//显示接收数据的类

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mEtUserName = findViewById(R.id.et_1);//找到et_1这个文本框
        mEtPassword = findViewById(R.id.et_2);

        initUI();//账号信息记录
        initData();//返回记录到的信息会输入框

        //线程，连接服务端拿数据（必须要开线程，会报错）
        //数据发送过早，如果用户更改登录信息，发送的还是之前的
        ClientSocket cs = new ClientSocket();
        cs.start();

        mBtnLogin = findViewById(R.id.btn_login);
        mBtnLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {//监听按钮

                //判断登陆成功的条件问问题，如果账号错误或者没有借过书，会卡死，
                while("".equals(sb.toString())){
                    //需要制作一个登陆等待的动画
                    Toast.makeText(MainActivity.this, "登录中", Toast.LENGTH_SHORT).show();
                }
                Toast.makeText(MainActivity.this, "登录成功", Toast.LENGTH_SHORT).show();
                //按下登录按钮后跳转到显示页面
                Intent intent = new Intent(MainActivity.this, TextViewActivity.class);
                startActivity(intent);
                tva.Setdata(sb);//把接收到的数据发到显示的类
            }
        });
    }

    public class ClientSocket extends Thread {
        public void run() {
            try {
                Socket s = new Socket("192.168.0.240", 6666);//服务端的ip地址，端口号

                //构建IO，用于接收和发送数据
                InputStream is = s.getInputStream();
                OutputStream os = s.getOutputStream();
                BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(os));

                //向服务器端发送一条消息
                for (int i = 0; i < 2; i++) {
                    bw.write(data[i]);
                }
                bw.flush();

                byte[] bytes = new byte[102400];//最大数据
                int len;
                String rcv_end = new String("-1");
                int tmp = 0;
                //接收数据
                while ((len = is.read(bytes)) != -1) {
                    String str = new String(bytes, 0, len, "UTF-8");
                    if (str.equals(rcv_end)) {//数据接收结束位
                        break;
                    }
                    sb.append(str );
                    //recData[tmp] = str;
                    //Log.e("aa",recData[tmp]);
                    //tmp = tmp + 1;
                    //System.out.println(sb);
                }

            } catch (UnknownHostException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private void initData(){
        if(sharedPreferences == null){
            sharedPreferences = getApplicationContext().getSharedPreferences("config", Context.MODE_PRIVATE);
        }
        //回写数据
        mEtUserName.setText(sharedPreferences.getString(SP_UserName, ""));
        mEtPassword.setText(sharedPreferences.getString(SP_PassWord, ""));
        mIsChecked = sharedPreferences.getBoolean(SP_REMEMBER_PSD, false);
        mCBPsd.setChecked(mIsChecked);
    }

    private void initUI(){
        mEtUserName.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
            }

            @Override
            public void afterTextChanged(Editable s) {
                if(mIsChecked){
                    if (sharedPreferences == null){
                        sharedPreferences = getApplicationContext().getSharedPreferences("config", Context.MODE_PRIVATE);
                    }
                    SharedPreferences.Editor edit = sharedPreferences.edit();
                    edit.putString(SP_UserName,mEtUserName.getText().toString());
                    edit.commit();
                }
                data[0] = mEtUserName.getText().toString();
            }
        });

        mEtPassword.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
            }

            @Override
            public void afterTextChanged(Editable s) {
                //文本改变之后记录用户记录用户密码
                if(mIsChecked){
                    if (sharedPreferences == null){
                        sharedPreferences = getApplicationContext().getSharedPreferences("config", Context.MODE_PRIVATE);
                    }
                    SharedPreferences.Editor edit = sharedPreferences.edit();
                    edit.putString(SP_PassWord, mEtPassword.getText().toString());
                    edit.commit();
                }
                data[1] = mEtPassword.getText().toString();
            }
        });

        mCBPsd = findViewById(R.id.cb_remember_psd);

        mCBPsd.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                Log.d("TAG","状态为：" +isChecked);
                mIsChecked = isChecked;
                if(isChecked){//判断是否点击CheckBox
                    //点击则保存
                    if (sharedPreferences == null){
                        sharedPreferences = getApplicationContext().getSharedPreferences("config", Context.MODE_PRIVATE);
                    }
                    SharedPreferences.Editor edit = sharedPreferences.edit();
                    edit.putString(SP_UserName,mEtUserName.getText().toString());
                    edit.putString(SP_PassWord, mEtPassword.getText().toString());
                    edit.putBoolean(SP_REMEMBER_PSD,isChecked);
                    //提交
                    edit.commit();
                }
            }
        });
    }

}