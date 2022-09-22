import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Fab from '@material-ui/core/Fab';
import NavigationIcon from '@material-ui/icons/Navigation';

const useStyles = makeStyles((theme) => ({
    margin: {
        margin: theme.spacing(1),
        marginLeft: theme.spacing(85),
        marginTop: theme.spacing(85 )
    },

    extendedIcon: {
        marginRight: theme.spacing(1),
    },
}));

export default function RoutingButton(props) {
    const classes = useStyles();

    return (
        <div onClick={props.onClick}>
            <div>
                <Fab variant="extended" color="primary" aria-label="add" className={classes.margin}>
                    <NavigationIcon className={classes.extendedIcon}/>
                    Get Route
                </Fab>
            </div>
        </div>
    );
}
