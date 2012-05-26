package org.psywerx.estudent;

import java.util.ArrayList;

import android.app.ListActivity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;

public class MenuActivity extends ListActivity{

	private static final int ACTION_LOGOUT = 0;
	private static final int ACTION_DISPLAY_MY_EXAMS = 1;
	private static final int ACTION_DISPLAY_EXAM_LIST = 2;

	protected static String username;
	protected static String password;
	protected static String firstname;
	protected static String lastname;
	protected static String userPIN;

	private ArrayList<MenuItem> mMenuItemsList = null;
	private MenuAdapter mMenuAdapter;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.menu_layout);
		mMenuItemsList = new ArrayList<MenuItem>();
		this.mMenuAdapter = new MenuAdapter(this, R.layout.menu_row, mMenuItemsList);
		setListAdapter(this.mMenuAdapter);

		getDataFromParent();
		fillMenuItems();
	}

	private void getDataFromParent(){
		Bundle b = getIntent().getExtras();
		username = b.getString("username");
		password = b.getString("password");
		firstname = b.getString("firstname");
		lastname = b.getString("lastname");
	}

	private void fillMenuItems(){
		mMenuItemsList = new ArrayList<MenuItem>();
		
		mMenuItemsList.add(new MenuItem("odjava","odjava iz sistema",
				ACTION_LOGOUT, MenuItem.LOGOUT_ICON));
		mMenuItemsList.add(new MenuItem("izpis","mojih izpitov",
				ACTION_DISPLAY_MY_EXAMS, MenuItem.NOTEPAD_ICON));
		mMenuItemsList.add(new MenuItem("izpis","izpitnih rokov",
				ACTION_DISPLAY_EXAM_LIST, MenuItem.NOTEPAD_ICON));

		D.dbgv("Menu items: "+ mMenuItemsList.size());

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
				finish();
				break;
			case ACTION_DISPLAY_MY_EXAMS:
				startMyExamsActivity();
				break;

			default:
				break;
			}
		}else{
			super.onListItemClick(l, v, position, id);
		}
	}

	private void startMyExamsActivity(){
		Intent intent = new Intent(this, AppliedExamsActivity.class);
		startActivity(intent);
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
				v = vi.inflate(R.layout.menu_row, null);
			}
			MenuItem o = items.get(position);
			if (o != null) {
				ImageView iv = (ImageView) v.findViewById(R.id.menu_row_image);
				TextView tt = (TextView) v.findViewById(R.id.toptext);
				TextView bt = (TextView) v.findViewById(R.id.bottomtext);
				if (tt != null){
					tt.setText(o.getItemName());                            }
				if (bt != null){
					bt.setText(o.getItemDescription());
				}
				if (iv != null){
					switch (o.getIcon()) {
					case MenuItem.LOGOUT_ICON:
						iv.setImageResource(R.drawable.logout_icon_128);
						break;
					case MenuItem.NOTEPAD_ICON:
						iv.setImageResource(R.drawable.notepad_icon_128);
						break;
					default:
						iv.setImageResource(R.drawable.setting_icon_128);
					}
				}
			}
			return v;
		}
	}
}
