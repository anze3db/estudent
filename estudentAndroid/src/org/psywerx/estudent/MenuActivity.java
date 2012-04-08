package org.psywerx.estudent;

import java.util.ArrayList;

import android.app.ListActivity;
import android.app.ProgressDialog;
import android.content.Context;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

public class MenuActivity extends ListActivity{

	private ProgressDialog m_ProgressDialog = null;
	private ArrayList<MenuItem> mMenuItemsList = null;
	private MenuAdapter mMenuAdapter;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.menu_layout);
		mMenuItemsList = new ArrayList<MenuItem>();
		this.mMenuAdapter = new MenuAdapter(this, R.layout.row, mMenuItemsList);
		setListAdapter(this.mMenuAdapter);

		fillMenuItems();
	}
	
	private void fillMenuItems(){
		mMenuItemsList = new ArrayList<MenuItem>();
		MenuItem o1 = new MenuItem();
		o1.setOrderName("User: lolIme");
		o1.setOrderStatus("logout");
		MenuItem o2 = new MenuItem();
		o2.setOrderName("izpiti");
		o2.setOrderStatus("pregled in odjava");
		mMenuItemsList.add(o1);
		mMenuItemsList.add(o2);
		
		D.dbgi("Menu items: "+ mMenuItemsList.size());
		
		if(mMenuItemsList != null && mMenuItemsList.size() > 0){
			mMenuAdapter.notifyDataSetChanged();
			for(int i=0;i<mMenuItemsList.size();i++)
				mMenuAdapter.add(mMenuItemsList.get(i));
		}
		mMenuAdapter.notifyDataSetChanged();
	}
	
	private class MenuAdapter extends ArrayAdapter<MenuItem> {

		private ArrayList<MenuItem> items;

		public MenuAdapter(Context context, int textViewResourceId, ArrayList<MenuItem> items) {
			super(context, textViewResourceId, items);
			this.items = items;
		}
		@Override
		public View getView(int position, View convertView, ViewGroup parent) {
			View v = convertView;
			if (v == null) {
				LayoutInflater vi = (LayoutInflater)getSystemService(Context.LAYOUT_INFLATER_SERVICE);
				v = vi.inflate(R.layout.row, null);
			}
			MenuItem o = items.get(position);
			if (o != null) {
				TextView tt = (TextView) v.findViewById(R.id.toptext);
				TextView bt = (TextView) v.findViewById(R.id.bottomtext);
				if (tt != null) {
					tt.setText(o.getOrderName());                            }
				if(bt != null){
					bt.setText(o.getOrderStatus());
				}
			}
			return v;
		}
	}
}