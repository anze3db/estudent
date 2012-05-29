package org.psywerx.estudent;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.psywerx.estudent.api.Api;
import org.psywerx.estudent.api.ResponseListener;
import org.psywerx.estudent.json.User;

import android.app.ListActivity;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.ContextMenu;
import android.view.ContextMenu.ContextMenuInfo;
import android.view.Menu;
import android.view.View;
import android.widget.ListView;
import android.widget.Toast;

public class MenuActivity extends ListActivity implements ResponseListener{
	
	private Context mContext;
	
	private static final int ACTION_LOGOUT = 0;
	private static final int ACTION_DISPLAY_MY_EXAMS = 1;
	private static final int ACTION_DISPLAY_ALL_EXAMS = 2;
		
	private MenuAdapter mMenuAdapter;
	private ProgressDialog mProgressDialog = null;
	private HashMap<Integer, String> mEnrollments = new HashMap<Integer, String>();
	private String mUsername;
	private ResponseListener mListener;
	
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		mContext = getApplicationContext();
		mListener = (ResponseListener) this;

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
		registerForContextMenu(getListView());
		
		Bundle extras = getIntent().getExtras();
		mUsername = extras.getString("username");
		setTitle(String.format("%s %s (%s)", extras.getString("firstname"), extras.getString("lastname"), mUsername));

	
		mEnrollments.put(1, "2010");
		mEnrollments.put(2, "kr neki");
		mEnrollments.put(1234, "zakaj");
	}
	
	@Override
	protected void onListItemClick(ListView l, View v, int position, long id) {
		super.onListItemClick(l, v, position, id);
		//Intent intent = null;
		switch (mMenuAdapter.getItem(position).getAction()) {
		case ACTION_DISPLAY_MY_EXAMS:
			//Toast.makeText(mContext, "prikazi izpite", Toast.LENGTH_SHORT).show();
			//intent = new Intent(mContext, ExamsActivity.class);
			//startActivity(intent);
			mProgressDialog = ProgressDialog.show(MenuActivity.this,    
					getString(R.string.loading_please_wait), 
					getString(R.string.loading_verifying_login), true);
			Api.examListRequest(mListener, mUsername);
			break;
		case ACTION_DISPLAY_ALL_EXAMS:
			//Toast.makeText(mContext, "prikazi izpite", Toast.LENGTH_SHORT).show();
			//intent = new Intent(mContext, ExamsActivity.class);
			//startActivity(intent);
			/*mProgressDialog = ProgressDialog.show(MenuActivity.this,    
					getString(R.string.loading_please_wait), 
					getString(R.string.loading_verifying_login), true);*/
			l.showContextMenuForChild(v);
			break;
		case ACTION_LOGOUT:
			finish();
			break;
		}
	}
	
	@Override
	public boolean onContextItemSelected(android.view.MenuItem item) {
		int ID = item.getItemId();
		//TODO
		Toast.makeText(mContext, "leto: "+ID, Toast.LENGTH_SHORT).show();
		Intent intent = new Intent(mContext, ExamsActivity.class);
		startActivity(intent);
		return true;
	}

	
	@Override
	public void onCreateContextMenu(ContextMenu menu, View v,
			ContextMenuInfo menuInfo) {
		super.onCreateContextMenu(menu, v, menuInfo);
		menu.setHeaderTitle(R.string.exams_contextTitle);
		for(Integer k: mEnrollments.keySet()) {
			menu.add(Menu.NONE, k, Menu.NONE, mEnrollments.get(k));
		}
	}

	public void onServerResponse(Object o) {
		mProgressDialog.dismiss();
		if(o == null)
			Log.d("majcn", "tega ni");
		else
			Log.d("majcn", o.getClass().getName());
	}
}