package com.example.cobalt;

import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.support.annotation.RequiresApi;
import android.support.v7.app.AppCompatActivity;
import android.view.View;

public class CameraActivity extends AppCompatActivity {

    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_camera);
        if (null == savedInstanceState) {
        getSupportFragmentManager().beginTransaction()
                .replace(R.id.camera_container, Camera2BasicFragment.newInstance())
                .commit();
        }
    }

    public void backToStreams(View view){
        Intent intent = new Intent(this, ViewAllStreams.class);
        startActivity(intent);
    }

    
}
