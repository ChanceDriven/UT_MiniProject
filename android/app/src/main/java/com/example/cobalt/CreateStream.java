package com.example.cobalt;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.Editable;
import android.view.View;
import android.widget.EditText;

public class CreateStream extends AppCompatActivity {

    EditText nameText;
    EditText emailText;
    EditText messageText;
    EditText tagsText;
    EditText coverUrlText;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_stream);
        nameText = (EditText)findViewById(R.id.editText);
        emailText = (EditText)findViewById(R.id.editText10);
        messageText = (EditText)findViewById(R.id.editText9);
        tagsText = (EditText)findViewById(R.id.editText8);
        coverUrlText = (EditText)findViewById(R.id.editText11);
    }

    public void createStream(View view){
        Editable name = nameText.getText();
    }
}
