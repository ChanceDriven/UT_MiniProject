package com.example.cobalt;

import android.content.Intent;
import android.preference.PreferenceActivity;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.RequestHandle;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.util.Formatter;
import java.util.Locale;

import cz.msebera.android.httpclient.Header;
import cz.msebera.android.httpclient.HttpEntity;
import cz.msebera.android.httpclient.entity.BasicHttpEntity;
import cz.msebera.android.httpclient.entity.StringEntity;

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

    public void createStream(View view) throws UnsupportedEncodingException {
        AsyncHttpClient httpClient = new AsyncHttpClient();
        String url = "https://fall-ut-apt.appspot.com/api_streams";

        String stringContent = String.format("{\"Name\":\"%s\",\"Emails\": \"%s\",\"Message\": \"%s\",\"Tags\": \"%s\",\"CoverUrl\": \"%s\"}",
                nameText.getText(), emailText.getText(), messageText.getText(), tagsText.getText(), coverUrlText.getText());

        HttpEntity content = new StringEntity(stringContent);
        httpClient.post(null, url, content, "text/json", new AsyncHttpResponseHandler() {

            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] responseBody) {
                // just go to the url
                String key = new String(responseBody);
                goToNewStream(key);
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, byte[] responseBody, Throwable error) {

            }
        });
    }

    public void goToNewStream(String key){
        Intent intent = new Intent(this, ViewStream.class);
        startActivity(intent);
    }
}
