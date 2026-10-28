import * as React from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import IconButton from '@mui/material/IconButton';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';
import MenuIcon from '@mui/icons-material/Menu';
import { useNavigate } from 'react-router';
import { useAuth } from '../auth/useAuth';

export default function TemporaryDrawer() {
  // Tracks the left drawer's open/close state
  const [isOpen, setIsOpen] = React.useState(false);
  const navigate = useNavigate();
  const { logout, user } = useAuth()


  const toggleDrawer =
    (open: boolean) =>
      (event: React.KeyboardEvent | React.MouseEvent) => {
        if (
          event.type === 'keydown' &&
          ((event as React.KeyboardEvent).key === 'Tab' ||
            (event as React.KeyboardEvent).key === 'Shift')
        ) {
          return;
        }

        setIsOpen(open);
      };

  const getRoutePath = (text: string) => {
    return `/${text.toLowerCase().replace(/\s+/g, '-')}`;
  };

  // The slide-out menu layout
  const list = () => (
    <Box
      sx={{ width: 250 }}
      role="presentation"
      onClick={toggleDrawer(false)}
      onKeyDown={toggleDrawer(false)}
    >
      <List>
        {['Profile', 'Coins', 'Markets', 'About'].map((text, index) => (
          <ListItem key={text} disablePadding>
            <ListItemButton onClick={() => {
              if (text == "Profile") {
                if (user) {
                  navigate(getRoutePath(text + `/${user?.id}`))
                } else {
                  navigate('/login', {
                    state: { message: "Please Login to view your profile." }
                  })
                }
              } else {
                navigate(getRoutePath(text))
              }
            }}
            >
              <ListItemIcon>
                {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
              </ListItemIcon>
              <ListItemText primary={text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <Divider />
      <List>
        {['Login', 'Signup', 'Logout'].map((text, index) => (
          <ListItem key={text} disablePadding>
            <ListItemButton onClick={() => {
              if (text == "Logout") {
                logout();
                navigate('/login');
              } else {
                navigate(getRoutePath(text));
              }
            }}>
              <ListItemIcon>
                {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
              </ListItemIcon>
              <ListItemText primary={text} />

            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box >
  );

  return (
    <header className="header">
      <div className="left-side">
        <IconButton
          onClick={toggleDrawer(true)}
          edge="start"
          aria-label="menu"
          sx={{ color: 'white' }} /* Inherits white from header styles */
        >
          <MenuIcon sx={{ fontSize: '2rem' }} />
        </IconButton>

        <Drawer
          anchor="right"
          open={isOpen}
          onClose={toggleDrawer(false)}
        >
          {list()}
        </Drawer>
      </div>

      {/* 2. MIDDLE: Kept for absolute positioning layout balancing */}
      <div className="middle">
        {/* Drop your center element or main app title here later */}
      </div>

      {/* 3. RIGHT SIDE: Kept clean for alignment balancing */}
      <div className="right-side">
        {/* Optional: Add profile icons or settings buttons here */}
      </div>
    </header>
  );
}
