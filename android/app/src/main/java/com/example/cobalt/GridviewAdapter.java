package com.example.cobalt;

import android.app.Activity;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by ebsaibes on 10/26/2017.
 */

public class GridviewAdapter extends BaseAdapter {

    private final Context context;
    private List<Stream> streams = new ArrayList<Stream>();



    public GridviewAdapter(Context context, List<Stream> streams){
        this.context = context;
        this.streams = streams;
    }

    @Override
    public int getCount() {
        return 0;
    }

    @Override
    public Stream getItem(int position) {

        return streams.get(position);
    }

    @Override
    public long getItemId(int position) {
        return 0;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        View MyView = convertView;

        if (MyView == null){
            //inflate the layout
            LayoutInflater layoutInflater = ((Activity) context).getLayoutInflater();
            MyView = layoutInflater.inflate(R.layout.activity_view_all_streams, null);
        }

        Stream stream = getItem(position);

        //TextView label = (TextView)MyView.findViewById(R.id.label)
        ImageView image = (ImageView) MyView.findViewById(R.id.grid_image);
        image.setScaleType(ImageView.ScaleType.CENTER_CROP);
        String url = stream.coverImgUrl;
        Picasso.with(context)
                .load(url)
                .placeholder(R.mipmap.ic_launcher)
                .error(R.mipmap.ic_launcher)
                .fit()
                .into(image);

        return MyView;

    }
}
