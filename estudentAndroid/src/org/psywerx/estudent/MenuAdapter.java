package org.psywerx.estudent;

import java.util.List;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

public class MenuAdapter extends ArrayAdapter<MenuItem> {
	
	private final List<MenuItem> mList;
	private final Context mContext;
	
	public MenuAdapter(Context context, List<MenuItem> list) {
		super(context, R.layout.menu_row, list);
		this.mContext = context;
		this.mList = list;
	}
	
	@Override
	public View getView(int position, View convertView, ViewGroup parent) {
		View rowView = convertView;
		if(rowView == null) {
			LayoutInflater inflater = (LayoutInflater) mContext.getSystemService(Context.LAYOUT_INFLATER_SERVICE);		
			rowView = inflater.inflate(R.layout.menu_row, parent, false);
		}
		ImageView vIcon = (ImageView) rowView.findViewById(R.id.icon);
		TextView vName = (TextView) rowView.findViewById(R.id.name);
		TextView vDesc = (TextView) rowView.findViewById(R.id.description);
		
		MenuItem item = mList.get(position);
		if(item.haveIcon())
			vIcon.setImageResource(item.getIcon());
		vName.setText(item.getName());
		vDesc.setText(item.getDescription());
		
		return rowView;
	}
}
