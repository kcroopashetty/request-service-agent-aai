# Testing Guide - New Features

## Prerequisites
1. Backend server running on port 8080
2. Frontend served via Live Server
3. Browser with developer tools open (F12)

---

## Test 1: Statistics Dashboard 📈

### Steps:
1. Open `index.html` in browser
2. Look at the top of the page

### Expected Result:
- 4 colorful stat cards displaying:
  - **Total** requests count
  - **Pending** requests count
  - **Approved** requests count
  - **Rejected** requests count

### Verify:
- Numbers match the actual request list below
- Cards have gradient backgrounds
- Stats update when you create/delete requests

---

## Test 2: Notification System 🔔

### Test 2A: Create Request Notification
1. Click **"+ Create Request"** button
2. Fill in form:
   - Request ID: `REQ-999`
   - Employee ID: Select any
   - Type: Select any
   - Status: Pending
3. Click **Submit**

**Expected:** Green success notification appears top-right: "Request created successfully!"

### Test 2B: Delete Request Notification
1. Click **🗑 Delete** on any request
2. Confirm deletion

**Expected:** Green success notification: "Request deleted successfully!"

### Test 2C: Error Notification
1. Try creating duplicate request ID
2. Or disconnect backend

**Expected:** Red error notification appears

### Verify:
- Notifications slide in from right
- Auto-dismiss after 3 seconds
- Can manually close with × button
- Multiple notifications stack vertically

---

## Test 3: Dark/Light Mode Toggle 🌓

### Steps:
1. Look at header - find moon icon button
2. Click the moon/sun icon

### Expected Result:
- **First click:** Switches to light mode
  - Background becomes white/light gray
  - Text becomes dark
  - Icon changes to sun ☀️
  
- **Second click:** Switches back to dark mode
  - Background becomes dark blue
  - Text becomes light
  - Icon changes to moon 🌙

### Verify:
1. Refresh page - theme persists
2. Check localStorage in DevTools:
   - Application → Local Storage
   - Should see `theme: "dark"` or `theme: "light"`

---

## Test 4: Export to CSV 📊

### Steps:
1. Ensure you have some requests in the list
2. Click **"Export CSV"** button (green button with download icon)

### Expected Result:
- CSV file downloads automatically
- Filename format: `requests_YYYY-MM-DD.csv`
- Green notification: "Data exported successfully!"

### Verify CSV Content:
1. Open downloaded CSV in Excel/Notepad
2. Should contain:
   - Headers: `request_id,employee_id,type,status,approver_by,created_at,updated_at`
   - All request data in rows
   - Proper CSV formatting with quotes

---

## Test 5: Enhanced UI/UX ✨

### Test 5A: No More Alert Popups
1. Create a request
2. Delete a request
3. Edit a request

**Expected:** No browser alert() popups - only smooth toast notifications

### Test 5B: Hover Effects
1. Hover over request cards
2. Hover over buttons

**Expected:** 
- Cards lift up slightly
- Buttons change color and lift
- Smooth transitions

---

## Test 6: Integration Test (All Features)

### Complete Workflow:
1. **Start:** Open dashboard in dark mode
2. **View Stats:** Check initial statistics
3. **Toggle Theme:** Switch to light mode
4. **Create Request:** 
   - Click "+ Create Request"
   - Fill form with `REQ-888`
   - Submit
   - See success notification
   - Stats update (+1 to Total and Pending)
5. **Export Data:**
   - Click "Export CSV"
   - Verify download
   - See success notification
6. **Delete Request:**
   - Delete REQ-888
   - See success notification
   - Stats update (-1 from Total and Pending)
7. **Toggle Theme:** Switch back to dark mode
8. **Refresh Page:** Verify theme persists

---

## Troubleshooting

### Issue: Stats not showing
- Check browser console for errors
- Verify backend is running
- Check `/request/` endpoint returns data

### Issue: Notifications not appearing
- Check if `notification-container` div exists in DOM
- Open DevTools → Elements → Search for "notification-container"
- Check console for JavaScript errors

### Issue: Theme not persisting
- Check browser localStorage is enabled
- Clear cache and try again
- Check DevTools → Application → Local Storage

### Issue: Export not working
- Check if requests array has data
- Verify browser allows downloads
- Check console for errors

### Issue: Import errors
- Ensure all files in `frontend/utils/` exist
- Check file paths are correct
- Verify script type="module" in HTML

---

## Quick Verification Checklist

- [ ] Stats cards visible and accurate
- [ ] Create request shows green notification
- [ ] Delete request shows green notification
- [ ] Theme toggle works (moon ↔ sun)
- [ ] Theme persists after refresh
- [ ] Export CSV downloads file
- [ ] Export shows success notification
- [ ] No alert() popups appear
- [ ] All buttons have hover effects
- [ ] Notifications auto-dismiss after 3s

---

## Browser Console Commands (Optional)

Test notifications manually:
```javascript
// In browser console
import notify from './utils/notifications.js';
notify.success("Test success!");
notify.error("Test error!");
notify.warning("Test warning!");
notify.info("Test info!");
```

Check theme:
```javascript
localStorage.getItem('theme')
```

---

**All tests passing? ✅ Your enhancements are working perfectly!**
