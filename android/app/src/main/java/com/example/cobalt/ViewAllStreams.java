package com.example.cobalt;

import android.nfc.Tag;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.GridView;
import android.widget.Toast;


import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.RequestHandle;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import cz.msebera.android.httpclient.Header;


public class ViewAllStreams extends AppCompatActivity {
    private static final String TAG = "ViewAllStreams";
    public String GET_ALL_STREAMS = "https://fall-ut-apt.appspot.com/api_streams";

    String streamid;
    String name;
    String coverImgURL;

    List<Stream> streams = new ArrayList<Stream>();




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_all_streams);
        getStreams();
        GridView gridview = (GridView) findViewById(R.id.all_streams_grid);

        gridview.setAdapter(new ImageAdapter(this));

        gridview.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            public void onItemClick(AdapterView<?> parent, View v,
                                    int position, long id) {
                Toast.makeText(ViewAllStreams.this, "" + position,
                        Toast.LENGTH_SHORT).show();
            }
        });

    }


    public void getStreams(){
        final String F_TAG = "getStreams";
        AsyncHttpClient httpClient = new AsyncHttpClient();
        Log.i(TAG, "getStreams: Async Task Spawned");



        RequestHandle allstreams = httpClient.get(GET_ALL_STREAMS, new AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] responseBody) {
                try{
                    Log.i(TAG, "getStreams: Success");
                    JSONObject jObj = new JSONObject(new String(responseBody));
                    JSONArray jArr = jObj.getJSONArray("all_Streams");
                    System.out.println(new String(responseBody));
                    Log.i(F_TAG,new String(responseBody));

                    for(int i =0; i< jArr.length(); i++){
                        JSONArray jStream = jArr.getJSONArray(i);
                        streamid = jStream.getString(0);
                        name = jStream.getString(1);
                        coverImgURL = jStream.getString(2);
                        Stream oStream = new Stream(streamid,name,coverImgURL);
                        streams.add(oStream);




                    }

                    createGridView(streams);


                }
                catch(JSONException je){
                    je.getCause();
                }
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, byte[] responseBody, Throwable error) {
                Log.e(F_TAG, "There was a problem in retrieving data : " + error.toString());
            }
        });

    }

    public void createGridView(List<Stream> streams) {

        GridView gridView = (GridView) findViewById(R.id.all_streams_grid);

        GridViewAdapter customGridAdapter = new GridViewAdapter(this, streams);

        //gridView.setAdapter(customGridAdapter);

        //gridView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
//
        //    public void onItemClick(AdapterView<?> parent, View v, int position, long id) {
        //        System.out.println("sid position:"+ position); //DEBUG
        //        showStream(v, position);
        //    }
        //});

    }


    /*
    class RetieveDataTask extends AsyncTask<Void, Void, String> {
        private Exception exception;

        @Override
        protected String doInBackground(Void... urls) {
            String data = "";
            // Do some validation here

            try{
                AsyncHttpClient httpClient = new AsyncHttpClient();



                HttpClient client = new DefaultHttpClient();
                HttpGet request = new HttpGet(API_URL);
                HttpResponse response = client.execute(request);
                BufferedReader rd = new BufferedReader
                        (new InputStreamReader(
                                response.getEntity().getContent()));
                String line = "";
                String returnStr = "";
                while ((line = rd.readLine()) != null) {
                    Log.i(TAG,line);

                }


            }
            catch (Exception ex){
                Log.e(TAG,ex.getMessage());
            }




            try {
                URL url = new URL(API_URL);
                HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                try {
                    BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                    StringBuilder stringBuilder = new StringBuilder();
                    String line;
                    while ((line = bufferedReader.readLine()) != null) {
                        stringBuilder.append(line).append("\n");
                    }
                    bufferedReader.close();
                    return stringBuilder.toString();
                } finally {
                    urlConnection.disconnect();
                }
            } catch (Exception e) {
                Log.e("ERROR", e.getMessage(), e);
                return null;
            }

        }
    }
    */

}
