package org.psywerx.estudent;

import java.util.ArrayList;

import android.app.ListActivity;
import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

public class MenuActivity extends ListActivity{

	private static final int ACTION_LOGOUT = 0;
	private static final int ACTION_DISPLAY_MY_EXAMS = 1;

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
		MenuItem o1 = new MenuItem("odjava","odjava iz sistema",ACTION_LOGOUT);
		MenuItem o2 = new MenuItem("izpis","izpis mojih izpitov",ACTION_DISPLAY_MY_EXAMS);
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

	@Override
	protected void onListItemClick(ListView l, View v, int position, long id) {
		MenuItem item = mMenuItemsList.get(position);
		if (item != null){
			D.dbgv("menu item pos: "+position+"  ime: "+item.getItemName());
			switch (item.getAction()) {
			case ACTION_LOGOUT:

				break;
			case ACTION_DISPLAY_MY_EXAMS:

				break;

			default:
				break;
			}
		}else{
			super.onListItemClick(l, v, position, id);
		}
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
					tt.setText(o.getItemName());                            }
				if(bt != null){
					bt.setText(o.getItemDescription());
				}
			}
			return v;
		}
	}
}
