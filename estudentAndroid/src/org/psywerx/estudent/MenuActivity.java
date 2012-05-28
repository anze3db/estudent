package org.psywerx.estudent;

import java.util.ArrayList;
import java.util.List;

import android.app.ListActivity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ListView;

public class MenuActivity extends ListActivity {
	
	private Context mContext;
	
	private static final int ACTION_LOGOUT = 0;
	private static final int ACTION_DISPLAY_MY_EXAMS = 1;
	private static final int ACTION_DISPLAY_ALL_EXAMS = 2;
		
	private MenuAdapter mMenuAdapter;
	
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		mContext = getApplicationContext();

		List<MenuItem> items = new ArrayList<MenuItem>();
		items.add(new MenuItem(
				getString(R.string.logout_name), 
				getString(R.string.logout_desc),  
				ACTION_LOGOUT, R.drawable.logout_icon_128));
		items.add(new MenuItem(
				getString(R.string.applied_exams_name), 
				getString(R.string.applied_exams_desc), 
				ACTION_DISPLAY_MY_EXAMS, R.drawable.notepad_icon_128));
		items.add(new MenuItem(
				getString(R.string.all_exams_list_name), 
				getString(R.string.all_exams_list_desc), 
				ACTION_DISPLAY_ALL_EXAMS, R.drawable.notepad_icon_128));
		
		mMenuAdapter = new MenuAdapter(mContext, items);
		setListAdapter(mMenuAdapter);
	}
	
	@Override
	protected void onListItemClick(ListView l, View v, int position, long id) {
		super.onListItemClick(l, v, position, id);
		Intent intent = null;
		switch (mMenuAdapter.getItem(position).getAction()) {
		case ACTION_DISPLAY_MY_EXAMS:
			//Toast.makeText(mContext, "prikazi izpite", Toast.LENGTH_SHORT).show();
			intent = new Intent(mContext, ExamsActivity.class);
			startActivity(intent);
			break;
		case ACTION_DISPLAY_ALL_EXAMS:
			//Toast.makeText(mContext, "prikazi izpite", Toast.LENGTH_SHORT).show();
			intent = new Intent(mContext, ExamsActivity.class);
			startActivity(intent);
			break;
		case ACTION_LOGOUT:
			finish();
			break;
		}
	}
}