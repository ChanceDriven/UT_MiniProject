package com.example.cobalt;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class ViewStream extends AppCompatActivity {
    Button subscribeButton;
    Button viewMoreButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_stream);
        subscribeButton = (Button)findViewById(R.id.button2);
        viewMoreButton = (Button)findViewById(R.id.button);
    }

    public void Subscribe(View view){

    }

    public void ViewMore(View view){

    }
}
